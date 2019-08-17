# `django_template_block_args`


## Motivation

This tool makes it easier to "componentize" your markup. Specifically, it makes it easier to create template tags that receive *blocks* as arguments. 


We've all written dialog markup that looks like this:

```django
  <div class="dialog dialog-success">
    <div class="dialog-success-icon"></div>
    <div class="dialog-content">
      Content goes here!
    </div>
  </div>
```

if you've written this more than once, you probably tried to create a template tag


```python
# templatetags.py
#...
@register.inclusion_tag('alert.html')
def dialog(type,content):
    return { 
      "type": type,
      "content": content,
    }

```

```django
<div class="dialog dialog-{{type}}>
  <div class="dialog-{{type}}-icon">
  </div>
  <div class="dialog-content"> {{content}} </div>
</div>
```

this would allow you to simply write 
```django
{% dialog 'success' 'Content goes here!' %} 
```

In your django templates, making it much more D.R.Y. The problem here is the inflexibility of what kind of content you can pass. If you want additional markup in the dialog, you're stuck repeating the markup everywhere or assembling markup within python strings and calling `mark_safe` on it. 

## Usage

django_template_block_args comes to the rescue by allowing you to pass entire blocks of template to a helper. It provides two functions, the simpler one covers most use-cases. This behaves a lot like django's builtin `register.inclusion_tag`. You can think of them as extensions to django's builtin `inclusion_tag`

### `register_composed_template(register, template_name, [takes_context=False])`

Working from our dialog example above, here's how we can pass blocks as arguments: 

```python
# templatetags.py
from django_template_block_args import register_composed_template
#...
@register_composed_template(register,'alert.html')
def dialog(type):
    return { 
      "type": type,
    }

```

```django
{% with var=True %}
{% dialog "success" %}
  Content goes here! No need to escape <strong> HTML </strong>, you can use template tags, filters and even access the surrounding template's context. 
  {% if var %}
    {% dialog "success" %} And recursion!  {% enddialog %}
  {% endif %}
{% enddialog %}
```

Note that we didn't pass nor receive the `context` argument as in the first example. That's because the child-block argument will automatically be merged into the target template's context as `content`. Make sure not to call any of your context variables content, because they will be overwritten by this default.    


### `register_composed_template_with_blockargs(register, template_name, block_names, [takes_context=False])`

`register_composed_template` only allows passing a single block, this other function allows passing *multiple* blocks, and naming them.

This can become useful when you want to populate a template with multiple pieces of text. For instance, we might have a card template component that looks like this:

```django
<div class="card card-{{type}}">
  {% if card_header %}
    <div class="card-header">
        {{card_header}}
    </div>
  {% endif %}
  <div class="card-body">
    {{card_body}}
  </div>
</div>

```

In order to pass blocks into `card_header` and `card_footer`, our python and consumer-template should look like:

```python
# templatetags.py
from django_template_block_args import register_composed_template
#...
@register_composed_template(register,'alert.html', block_names=("card_header", "card_body"))
def card(type):
  # note that block-args automatically get passed to the template
    return {"type":type}

```

```django
{% card "success" %}
  {% blockarg 'card_body' %}
    I'm a card-body!
  {% endblockarg %}
  {% blockarg 'card_header' %}
    I'm a card-header!
  {% endblockarg %}
{% enddialog %}
```

just like the first example, the header and footer blocks can also contain markup, template tags, and access the surrounding context.


## Installation

```bash
pip install django-template-block-args
```

This package consists of 2 simple functions whose only dependencies are built-in django. All you need is to import these functions into your existing templatetags module. No need to change anything in your django settings module.


## developing 

1. The repo contains the package's module, and an example django project 


## Contributing/Next steps
1. Write tests
2. A short list of examples to replace the docs above 
3. Better error signaling
    * Make sure people avoid using template content in between a custom-tag and its block-args
    * should not use block-names or content in the function