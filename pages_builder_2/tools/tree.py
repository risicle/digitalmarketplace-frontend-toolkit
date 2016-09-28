class Tree(object):
    """Reads and holds information on a patterns directory structure"""
    def __init__(self, paths_to_ignore):
        self._tree = {}
        self.paths_to_ignore = paths_to_ignore

    def get_node(self, steps):
        current_node = self._tree
        for step in steps:
            if 'children' in current_node:
                current_node = current_node['children'][step]
            else:
                current_node = current_node[step]
        return current_node

    def add(self, path, dirs=[], files=[]):
        def allow_path(path):
            for pattern in self.paths_to_ignore:
                if pattern.match(path) is not None:
                    return False
            return True

        # adding the root node
        if path == '':
            self._tree = {dir: {} for dir in dirs if allow_path(dir)}
            return

        steps = path.split('/')
        node = self.get_node(steps)
        node['files'] = files
        if len(dirs) > 0:
            # create child nodes for each directory in this node
            node['children'] = {dir: {} for dir in dirs if allow_path(dir)}

    def get(self, path):
        if len(path) > 0:
            return self.get_node(path.split('/'))
        else:
            return self._tree
