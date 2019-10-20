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
@register.inclusion_tag('dialog.html')
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

In your django templates, making it much more D.R.Y. The problem here is the inflexibility of what kind of content you can pass. If you want additional markup, or you want to call another helper in the dialog, you're stuck repeating the markup everywhere or assembling markup within python strings and calling `mark_safe` on it.

An extremely frequent problem of this sort is multi-line string literals, or calling an internationalization helper.  

## Usage

django_template_block_args comes to the rescue by allowing you to pass entire blocks of template to a helper. It provides two functions, the simpler one covers most use-cases. This behaves a lot like django's builtin `register.inclusion_tag`. You can think of them as extensions to django's builtin `inclusion_tag`

### `register_composed_template(register, template_name, [takes_context=False])`

Working from our dialog example above, here's how we can pass blocks as arguments: 

```python
# templatetags.py
from django_template_block_args import register_composed_template
#...
@register_composed_template(register,'dialog.html')
def dialog(type):
    return { 
      "type": type,
    }

```

```django
{% dialog "success" %}
  Content goes here! No need to escape <strong> HTML </strong>, you can use template tags, filters and even access the surrounding template's context. 
  {% if some_var_in_scope %}
    {% dialog "success" %} And recursion!  {% enddialog %}
  {% endif %}
{% enddialog %}
```

Note that we didn't pass nor receive the `content` argument as in the first example. By convention, the child-block argument will automatically be merged into the target template's context as `content`. Make sure not to call any of your context variables content, because they will be overwritten by this default.


### `register_composed_template_with_blockargs(register, template_name, block_names, [takes_context=False])`

`register_composed_template` only allows passing a single block, but this function allows passing *multiple* blocks, with variable names.

This is useful when you want to populate a template with multiple pieces of text. For instance, we might have a card template component that looks like this:

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

In order to pass separate blocks into `card_header` and `card_footer`, here's what our python and consumer-template should look like:

```python
# templatetags.py
from django_template_block_args import register_composed_template_with_blockargs
#...
@register_composed_template_with_blockargs(register,'card.html', block_names=("card_header", "card_body"))
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
{% endcard %}
```

just like the first example, the header and footer blocks can also contain markup, template tags, and access the surrounding context.

### Pitfalls/gotchas

#### Don't put anything between the component "root" call and its named blocks

Currently, you can't put any templatetags or text between a component's root node and its named block-args. For instance, the following is invalid and will throw an exception.

```django
  {% card "success" %}
    {% if header %}
      {%  blockarg 'card_header' %}
        some header
      {% endblockarg %}
    {% endif %}
  {% endcard %}
```

#### whitespace is truthy

In the card example above, the `{% if header %}` will evaluate to true even if header is a bunch of whitespace/newline characters. Since our `card.html` only checks if `header` is truthy, the following will always result in the `<div class="card-header">...` markup being rendered.

```django
{% card %}
  {% block_arg card_header %}
    {{ "" }}
  {% endblockarg %}
{% endcard %}
```

Why? Because the card_header doesn't just get passed what's in the double-brackets, but also the newlines and indentation spaces that make our template. The following would not result in a truthy card_header argument, but it looks terrible.

```django
{% card %}
  {% block_arg card_header %}{{ "" }}{% endblockarg %}
{% endcard %}
```

To get around this without writing ugly templates, you can define a filter that checks for non-whitespace:


```python 
@register.filter
def has_content(safetext):
  if not safetext:
    return False
  str = safetext+""
  return len(str.strip())
```

this would require modifying the card template's from `if header` tag to `{% if header|has_content %}`.

#### blocks are not lazily evaluated

Behind the scenes, your block args are rendered as normal content *before* being passed to the template helper. Even if your component's template uses conditionals, you can't assume the "falsey" branches don't get rendered. This can cause issues if you use template helpers that perform side-effects or are expensive (e.g. run queries). There's no perfect workaround here, but rest assured you can use conditionals within the passed block itself and the templating system will use standard conditional rendering.  

## Installation

```bash
pip install django-template-block-args
```

This package consists of 2 simple functions whose only dependencies are built-in django. All you need is to import these functions into your existing templatetags module. No need to change anything in your django settings module.


## developing 

This repo contains the package's module, and an example django project. Dependencies are installed using pipenv. You can run tests using the familiar `./manage.py test`. 


## Contributing/Next steps
1. Write a "with_block_as" helper can help with more ad-hoc cases 
  * for instance, if I don't want the footprint of creating another templatetag, but I want to pass a rendered block as an argument to an already existing tag 
2. Allow nesting named blocks inside conditionals (difficult)
3. Write better tests
4. A short list of examples to replace the docs above 
5. Better error signaling