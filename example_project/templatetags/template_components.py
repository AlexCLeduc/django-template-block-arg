from django import template
from django.template.library import InclusionNode
from django.utils.safestring import mark_safe

from django_template_block_args import register_composed_template, register_composed_template_with_blockargs

register = template.Library()
  
@register.simple_tag()
def obj_class_name(obj):
   return obj.__class__.__name__


# @register.tag('balert')
# def do_alert(parser, token):
#     import IPython; IPython.embed()
#     tokens =token.split_contents()
#     if len(tokens) != 2:
#         raise template.TemplateSyntaxError("this tag requires a single argument")
#     alert_type = tokens[1]
#     # import IPython; IPython.embed()
#     # if not (alert_type[0] == alert_type[-1] and alert_type[0] in ('"', "'")):
#       # raise template.TemplateSyntaxError("this tag requires a string argument")

#     nodelist = parser.parse(('endbalert',))
#     parser.delete_first_token()
#     # return AlertNode(nodelist, alert_type[1:-1])
#     def get_context(context):
#         alert_modifier = {
#             "danger": "alert-danger",
#             "success": "alert-success",
#         }.get(alert_type, "")
#         alert_cls = f"alert {alert_modifier}"
#         new_args = {
#             "content": nodelist.render(context),
#             "alert_cls":  alert_cls,
#         }
#         # TODO: figure out how to pass (some) context down
#         # ideally, just the request-based context coming from processors, and NOT stuff like aliases defined around the template 

#         return new_args 
#     return InclusionNode(
#       get_context,
#       True,
#       [],
#       {},
#       "alert.html",
#     )


# class AlertNode(template.Node):
#     def __init__(self,nodelist,alert_type=None):
#       super().__init__()
#       self.nodelist = nodelist
#       self.alert_type = alert_type

#     def render(self, context):
#         alert_modifier = {
#             "danger": "alert-danger",
#             "success": "alert-success",
#         }.get(self.alert_type, "")
        
#         alert_cls = f"alert {alert_modifier}"
        
#         return f"""
#           <div class="{alert_cls}">
#             {self.nodelist.render(context)}
#           </div>
#         """

# @register.inclusion_tag('alert.html')
# def simple_alert(alert_type,content):
#     alert_modifier = {
#         "danger": "alert-danger",
#         "success": "alert-success",
#     }.get(alert_type, "")
#     alert_cls = f"alert {alert_modifier}"
#     return {
#         "alert_cls": alert_cls,
#         "content": content,
#     }

@register_composed_template(register,'alert.html')
def alert(type):
    alert_modifier = {
        "danger": "alert-danger",
        "success": "alert-success",
    }.get(type, "")
    alert_cls = f"alert {alert_modifier}"
    return {
        "alert_cls": alert_cls,
    }


@register.simple_tag()
def my_lorem_ipsum():
    return mark_safe(f"<strong> lorem ipsum </strong>")



@register_composed_template(register,"panel.html", takes_context=True)
def panel(context,title=None, include_nested_panel=False):
    return {
        "title": title,
        "include_nested_panel": include_nested_panel,
    }


@register_composed_template_with_blockargs(
    register,
    "complex-panel.html",
    block_names=(
        "panel_header",
        "panel_footer",
        "panel_footer",
    )
)
def complex_panel(panel_type):
    return {
        "panel_type": panel_type,
    }