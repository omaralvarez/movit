from django import template

register = template.Library()

@register.inclusion_tag('tooltip.html')
def tooltip(color, text, type):
    return {'color': color, 'text': text, 'type': type}

@register.inclusion_tag('tooltip_js.html')
def activate_tooltip():
    return {}

@register.inclusion_tag('dropdown.html')
def dropdown(state, id, text):
    return {'state': state, 'id': id, 'text': text}

@register.inclusion_tag('dropdown_js.html', takes_context=True)
def activate_dropdown(context):
    return {}
