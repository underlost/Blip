from __future__ import absolute_import

from django import template
from .models import Entry

class EntryListNode(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        context[self.varname] = Entry.objects.filter(is_private=False)
        return ''

def do_get_entry_list(parser, token):
    #{% get_entry_list as entry_list %}
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
    if bits[1] != "as":
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
    return EntryListNode(bits[2])

register = template.Library()
register.tag('get_entry_list', do_get_entry_list)
