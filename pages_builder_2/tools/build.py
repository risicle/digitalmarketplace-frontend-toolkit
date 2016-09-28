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

    def resources_to_ignore(self, as_paths=False, as_regexes=False):
        resources = [
            (self.src, 'tools'),
            (self.src, 'templates'),
            (self.src, 'govuk_template')
        ]
        if as_paths is True:
            return [
                os.path.join(resource[0], resource[1])
                for resource in resources]
        elif as_regexes is True:
            return [
                re.compile(os.path.join(resource[0], resource[1]))
                for resource in resources]
        else:
            return resources

    def _filter(self, dir, contents):
        filter_out = []
        for file in self.resources_to_ignore():
            if dir is file[0] and file[1] in contents:
                filter_out.append(file[1])
        return filter_out

    def create_tree(self):
        if os.path.exists(self.dst):
            shutil.rmtree(self.dst)

        copytree(self.src, self.dst, ignore=self._filter)

    def render_pages(self):
        paths_to_ignore = self.resources_to_ignore(as_regexes=True)
        tree = Tree(paths_to_ignore)

        def allow_path(path):
            for pattern in paths_to_ignore:
                if pattern.match(path) is not None:
                    return False
            return True

        for root, dirs, files in os.walk(self.src):
            if allow_path(root):
                print('root before: {}'.format(root))
                print('root after: {}'.format(root.replace(self.src, '')))
                tree.add(root.replace(self.src, ''), dirs, files)
            return tree
