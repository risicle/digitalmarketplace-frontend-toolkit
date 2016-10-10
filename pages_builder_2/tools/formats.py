import os
import abc
import yaml


class Page(object):
    __metaclass__ = abc.ABCMeta

    def _get_data_from_yaml(self, filename):
        with open(os.path.join(self.src_root, filename), 'r') as file:
            contents = file.read()
        return yaml.load(contents)

    def __init__(self, src_root, env):
        self.src_root = src_root
        self.dst_root = dst_root
        self.template_env = env
        self.data = self.get_data()

    @abc.abstractmethod
    def get_data(self):
        """Get the data used to render the page"""
        return

    @abc.abstractmethod
    def render(self):
        """Render the page and return it"""
        return


class Index(Page):
    def get_data(self):
        data = []
        return data

    def render(self):
        # get templates for pattern
        template = template_env.get_template(
            os.path.join(self.src_root, 'index'))
        return template.render(self.data)

    def is_pattern(self, dir_path):
        return os.path.exists(os.path.join(dir_path, 'examples'))


class Pattern(Page):
    def get_data(self):
        # build data from manifests for meta and examples
        data = self._get_data_from_yaml('meta.yml')
        examples = self._get_data_from_yaml('examples.yml')
        data['examples'] = examples
        return data

    def render(self):
        # get templates for pattern
        template = template_env.get_template(
            os.path.join(self.src_root, 'pattern'))
        return template.render(self.data)
