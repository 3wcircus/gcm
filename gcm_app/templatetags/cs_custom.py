import re

from django import template
from django.template.defaultfilters import stringfilter

# A few custom filters for use in templates
register = template.Library()


# Part of support for using variables in templates
class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""


# Quick and dirty custom template that supports defining/using variables in the Django templates
@register.tag(name='set')
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])


# Quick and dirty custom filter that will let u execute a regular expression from Django template
# TODO: Enhance this so you can get back more than one capturing group
@register.filter
@stringfilter
def regex1(value, exp):
    match = re.search(exp, value, re.IGNORECASE)
    if match:
        result = match.group(1)
    else:
        result = ""
    return result
