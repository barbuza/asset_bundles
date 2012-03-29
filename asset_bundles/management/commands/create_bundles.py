# -*- coding: utf-8 -*-

import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.template import Template
from django.template.base import TemplateSyntaxError

from ...templatetags.assets import AssetsNode


def get_django_template_dirs():
    """Build a list of template directories based on configured loaders.
    """
    template_dirs = []
    if 'django.template.loaders.filesystem.load_template_source' in\
                                                settings.TEMPLATE_LOADERS or\
       'django.template.loaders.filesystem.Loader' in\
                                                settings.TEMPLATE_LOADERS:
        template_dirs.extend(settings.TEMPLATE_DIRS)
    if 'django.template.loaders.app_directories.load_template_source' in\
                                                settings.TEMPLATE_LOADERS or\
       'django.template.loaders.app_directories.Loader' in\
                                                settings.TEMPLATE_LOADERS:
        from django.template.loaders.app_directories import app_template_dirs
        template_dirs.extend(app_template_dirs)
    return template_dirs


def collect_templates(path):
    templates = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(".html"):
                templates.append(os.path.join(dirpath, filename))
    return templates


class Command(BaseCommand):
    
    help = "creates bundles from django templates"
    
    def handle(self, *args, **options):
        for path in get_django_template_dirs():
            for template in collect_templates(path):
                self.process_template(template)
    
    def process_template(self, template):
        with open(template) as fp:
            try:
                tmpl = Template(fp.read().decode("utf-8"))
            except UnicodeDecodeError:
                print "skipping %r - it has non-unicode symbols" % template
                return
            except TemplateSyntaxError as err:
                print "skipping %r - it has sytax error %r" % (template, err)
                return
        result = []
        def _recurse_node(node):
            if node is not None and isinstance(node, AssetsNode):
                try:
                    bundle = node.resolve()
                except template.VariableDoesNotExist:
                    raise LoaderError('skipping bundle %s, depends on runtime data' % node.output)
                else:
                    result.append(bundle)
            for subnode in hasattr(node, 'nodelist') \
                and node.nodelist\
                or []:
                    _recurse_node(subnode)
        for node in tmpl:
            _recurse_node(node)
        if result:
            print template
            for bundle in result:
                bundle.respect_debug = False
                print "\t%s" % list(bundle.urls)[0]
    