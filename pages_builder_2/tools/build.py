import os
import re
from shutil import copytree, rmtree, ignore_patterns
from jinja2 import Environment, FileSystemLoader
from dmutils.filters import markdown_filter
from tree import Tree


class Structure(object):
    def _set_template_env(self):
        env = Environment(loader=FileSystemLoader(self.src))
        env.filters.update({
            'markdown': markdown_filter
        })
        # used in `toolkit/templates/summary-table.html`
        # for a conditional import statement
        env.globals['PAGES_BUILDER'] = True
        env.add_extension('jinja2.ext.with_')
        return env

    def __init__(self, src_dir, dst_dir):
        root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..'))

        self.src = os.path.join(root, src_dir)
        self.dst = os.path.join(root, dst_dir)
        self.template_env = self._set_template_env()
        self.tree = self.get_tree(self)

    def get_tree(self):
        for root, dirs, files in os.walk(self.src):
            print('root before: {}'.format(root))
            print('root after: {}'.format(root.replace(self.src, '')))
            tree.add(root.replace(self.src, ''), dirs, files)
        return tree

    def get_format(node):
        if 'children' in node:
           return Index(node)
        elif 'examples' in node:
           return Pattern(node)
        return false

    def create_pages(self):
        if os.path.exists(self.dst):
            shutil.rmtree(self.dst)

        for node in self.tree.get_nodes():
            format = self.get_format(node)
            src_path = os.path.join(self.src, path)
            dst_path = os.path.join(self.dst, path)
            if format:
                # create directory for page
                shutil.copy(src_path, dst_path)
                # render page
                format.render(dst_path)
