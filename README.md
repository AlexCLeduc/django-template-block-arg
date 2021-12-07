[![CircleCI](https://circleci.com/gh/AlexCLeduc/django-template-block-arg.svg?style=shield)](https://circleci.com/gh/AlexCLeduc/django-template-block-arg)
# django-template-block-args


## Motivation

This tool facilitates creating template tags that receive *blocks* as arguments. 


We've all written alert markup that looks like this:

```django
  <div class="alert alert-success">
    <div class="alert-success-icon"></div>
    <div class="alert-content">
      Success message
    </div>
  </div>
```

If you repeat the surrounding markup often, you might want to write a template tag:


```python
# ... templatetags.py
@register.inclusion_tag('alert.html')
def alert(type,content):
    return { 
      "type": type,
      "content": content,
    }

```


This would allow you to D.R.Y out your django templates and simply write
```django
{% alert 'success' 'Success message' %} 
```

Unfortunately this is inflexible. If you want to pass markup, or the result of another helper in the alert, you need to create an extra template-tag or have your views  create process string content.

An extremely frequent problem of this sort is multi-line string literals, or calling an internationalization helper.  

## Usage

django_template_block_args allows you to pass blocks of template code to a helper. It provides two functions, the simpler one covers most use-cases. This behaves a lot like django's builtin `register.inclusion_tag`.

### `register_composed_template(register, template_name, [takes_context=False])`

Working from our alert example above, here's how we can pass blocks as arguments: 

```python
# templatetags.py
from django_template_block_args import register_composed_template
#...
@register_composed_template(register,'alert.html')
def alert(type):
    return { 
      "type": type,
    }

```

```django
{% alert "success" %}
  Content gets passed as a block. No need to escape <strong> HTML </strong>, you can use template tags, filters and even access the surrounding template's context. 
  {% if some_var_in_scope %}
    {% alert "success" %} Even recursion works  {% endalert %}
  {% endif %}
{% endalert %}
```

Note that we didn't pass nor receive the `content` argument as in the first example. By convention, the child-block argument will automatically be merged into the target template's context as `content`. Make sure not to call any of your context variables content, because they will be overwritten by this default.


### `register_composed_template_with_blockargs(register, template_name, block_names, [takes_context=False])`

The former `register_composed_template` only allows passing a single block called `content`, but this function allows passing *multiple* blocks, with other names.

This is useful when you want to populate a template with multiple pieces of text. For instance, we might have a card template component that looks like this:

```django
<div class="card card-{{type}}">
  {% if card_header %}
    <div class="card-header">
        {{header}}
    </div>
  {% endif %}
  <div class="card-body">
    {{body}}
  </div>
</div>

```

In order to pass separate blocks into `header` and `body`, here's what our python and consumer-template should look like:

```python
# templatetags.py
from django_template_block_args import register_composed_template_with_blockargs
#...
@register_composed_template_with_blockargs(register,'card.html', block_names=("header", "body"))
def card(type):
    # block-args automatically get passed to the template's context
    return {"type":type}

```

```django
{% card "success" %}
  {% blockarg 'header' %}
    I'm a card-header
  {% endblockarg %}
  {% blockarg 'body' %}
    I'm a card-body with <br/> markup
  {% endblockarg %}
{% endcard %}
```

just like the alert example, the header and body blocks can also contain markup, template tags, and access the surrounding context.

## Pitfalls/gotchas

### **Don't put anything between the component "root" call and its named blocks**

Currently, you can't put any templatetags or text between a component's root node and its named block-args. For instance, the following is invalid and will throw an exception.

```django
  {% card "success" %}
    {% if cond %}
      {%  blockarg 'header' %}
        some header
      {% endblockarg %}
    {% endif %}
  {% endcard %}
```

### **whitespace is truthy**

In the card example above, the `{% if header %}` will evaluate to true even if header is a bunch of whitespace/newline characters. Since our `card.html` only checks if `header` is truthy, the following will always result in the `<div class="card-header">...` markup being rendered.

```django
{% card %}
  {% block_arg header %}
    {{ "" }}
  {% endblockarg %}
{% endcard %}
```

Why? Because the card_header doesn't just get passed what's in the double-brackets, but also the newlines and indentation spaces around it. The following workaround would not result in a truthy `header` argument, but it looks terrible.

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

### **blocks are not lazily evaluated**

Behind the scenes, your block args are rendered as normal content *before* being passed to the template helper. Even if your component's template uses conditionals, you can't assume the "falsey" branches don't get rendered. This can cause issues if you use template helpers that perform side-effects or are expensive (e.g. run queries). There's no perfect workaround here, but rest assured you can use conditionals within the passed block itself and the templating system will use standard conditional rendering.  

## Installation

```bash
pip install django-template-block-args
```

This package consists of 2 simple functions whose only dependencies are built-in django. All you need is to import these functions into your existing templatetags module. No need to change anything in your django settings module.


## developing 

This repo contains the package's module, and an example django project. Dependencies are installed using pipenv. You can run tests using the familiar `./manage.py test`. 


## Contributing/Next steps
1. Write a "block_alias" helper to map a block to a variable consumable by vanilla template tags
  ```django
    {% block_alias varname %}
      some block content
    {% endwith_block_as %}

    {% some_vanilla_tag varname %}
  ```
2. Write better tests
3. Better error signaling