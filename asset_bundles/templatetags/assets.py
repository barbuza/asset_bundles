# -*- coding: utf-8 -*-

from django import template
from django.conf import settings

from ..bundle import Bundle


register = template.Library()


class AssetsNode(template.Node):
    
    def __init__(self, type_, output, files, childnodes):
        self.childnodes = childnodes
        self.output = output
        self.files = files
        self.type = type_

    def resolve(self, context={}):
        
        def resolve_var(x):
            if x is None:
                return None
            else:
                try:
                    return template.Variable(x).resolve(context)
                except template.VariableDoesNotExist, e:
                    raise
        
        def resolve_bundle(name):
            try:
                return get_env()[name]
            except KeyError:
                return name
        
        return Bundle(resolve_var(self.type),
                      [resolve_var(f) for f in self.files],
                      resolve_var(self.output))

    def render(self, context):
        bundle = self.resolve(context)
        
        result = u""
        for url in bundle.urls:
            context.update({"ASSET_URL": settings.STATIC_URL + url})
            try:
                result += self.childnodes.render(context)
            finally:
                context.pop()
        return result


def assets(parser, token):
    type_ = None
    output = None
    files = []
    args = token.split_contents()[1:]
    for arg in args:
        if arg[-1] == ",":
            arg = arg[:-1]
            if not arg:
                continue
        arg = arg.split("=", 1)
        if len(arg) == 1:
            name = None
            value = arg[0]
        else:
            name, value = arg
        if name == "output":
            output = value
        elif name == "type":
            type_ = value
        elif name is None:
            files.append(value)
        else:
            raise template.TemplateSyntaxError("Unsupported keyword"
                                               " argument \"%s\"" % name)
    childnodes = parser.parse(("endassets", ))
    parser.delete_first_token()
    return AssetsNode(type_, output, files, childnodes)


register.tag("assets", assets)
