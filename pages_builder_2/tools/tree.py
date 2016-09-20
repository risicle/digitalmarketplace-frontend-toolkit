class Tree(object):
    """Reads and holds information on a patterns directory structure"""
    def __init__(self):
        self._tree = {}

    def get_node(self, steps):
        current_node = self._tree
        for step in steps:
            if 'children' in current_node:
                current_node = current_node['children'][step]
            else:
                current_node = current_node[step]
        return current_node

    def add(self, path, dirs=[], files=[]):
        steps = path.split('/')
        if len(steps) == 1:
            self._tree[steps[0]] = {}
            node = self._tree[steps[0]]
        else:
            node = self.get_node(steps)
        # node is pattern
        if 'examples' in dirs:
            node['type'] = 'pattern'
            node['examples'] = []
        # node is examples dir in a pattern
        elif steps[-1] == 'examples':
            node += files
        # node is section
        else:
            node['type'] = 'section'
            # create child nodes for each directory in this node
            node['children'] = {dir: {} for dir in dirs}

    def get(self, path):
        return self.get_node(path.split('/'))
