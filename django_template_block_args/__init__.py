import functools

from django import template
from django.template.library import InclusionNode
from django.template.context import make_context
from django.utils.safestring import mark_safe
from django.template.library import getfullargspec, parse_bits

from django.template.defaulttags import IfParser

def register_composed_template(register,filename, func=None, name=None, takes_context=None):
    
  def dec(func):
      params, varargs, varkw, defaults, kwonly, kwonly_defaults, _ = getfullargspec(func)
      function_name = (name or getattr(func, '_decorated_function', func).__name__)

      @functools.wraps(func)
      def compile_func(parser,token):
          bits = token.split_contents()[1:]

          # TODO: figure out if this is lazy/thread-safe
          nodelist = parser.parse((f"end{function_name}",))
          parser.delete_first_token()

          args, kwargs = parse_bits(
              parser, bits, params, varargs, varkw, defaults,
              kwonly, kwonly_defaults, takes_context, function_name,
          )
          def _func(context,*args,**kwargs):
              if takes_context:
                  ret = func(context, *args,**kwargs)
              else:
                  ret = func(*args,**kwargs)

              return {
                  **ret,
                  "content": nodelist.render(context)
              }

          return InclusionNode(
              _func,
              True, # takes_context, there are 2 different kinds of context here
              args,
              kwargs,
              filename
          )
      register.tag(function_name,compile_func)
      return func

  return dec



def register_composed_template_with_blockargs(register,filename, func=None, name=None, takes_context=None, block_names=None):
    if not block_names:
        raise Exception("Must have block names")
    
    def dec(func):
        params, varargs, varkw, defaults, kwonly, kwonly_defaults, _ = getfullargspec(func)
        function_name = (name or getattr(func, '_decorated_function', func).__name__)
  
        @functools.wraps(func)
        def compile_func(parser,token):
            bits = token.split_contents()[1:]
  
            # TODO: figure out if this is lazy/thread-safe
            # parser.delete_first_token()
            
            token = parser.next_token()
            
            nodelists_by_name = {}
            
            end_tag_token = f"end{function_name}"

            blocks_left = len(block_names) + 1 # +1 for the eng_tag_token
            while blocks_left:
                useless = parser.parse(("blockarg",end_tag_token))
                token = parser.next_token()
                if token.contents.startswith(end_tag_token):
                    blocks_left = 0
                    for name in block_names:
                        if name not in nodelists_by_name:
                            nodelists_by_name[name] = None
                else: # {% block_arg <block_name> %}
                    block_name = token.split_contents()[1][1:-1] # TODO: make it clear that this needs to be a literal string ""/ '' and not a variable
                    block_nodelist = parser.parse(f"endblockarg")
                    nodelists_by_name[block_name] = block_nodelist
                    token = parser.next_token()
                    blocks_left = blocks_left - 1
                            
  
            args, kwargs = parse_bits(
                parser, bits, params, varargs, varkw, defaults,
                kwonly, kwonly_defaults, takes_context, function_name,
            )
            def _func(context,*args,**kwargs):
                if takes_context:
                    ret = func(context, *args,**kwargs)
                else:
                    ret = func(*args,**kwargs)
  
                return {
                    **ret,
                    **{
                        name: nodelist and nodelist.render(context)
                        for (name,nodelist) in nodelists_by_name.items() 
                    }
                }
  
            return InclusionNode(
                _func,
                True, # takes_context, there are 2 different kinds of context here
                args,
                kwargs,
                filename
            )
        register.tag(function_name,compile_func)
        return func
  
    return dec
  
  

