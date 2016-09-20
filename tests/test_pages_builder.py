import sys
import os
import shutil

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
builder_dir = os.path.join(root, 'pages_builder_2')
template_dir = os.path.join(builder_dir, 'templates')
sys.path.append(builder_dir)

from tools import build, tree

def _clean(folders):
    for dir in folders:
        if os.path.exists(os.path.join(root, dir)):
            shutil.rmtree(dir)

class TestTree(object):
    tree = tree.Tree()

    def test_adding_a_pattern_dir(self):
        level_1_node_1_examples = os.path.join('node_1', 'examples')
        self.tree.add(
            'node_1',
            dirs=['examples'])
        self.tree.add(
            level_1_node_1_examples,
            files=['example_1.html', 'example_2.html'])
        assert self.tree.get('node_1') == {
            'type' : 'pattern',
            'examples' : [
                'example_1.html',
                'example_2.html'
            ]
        }

    def test_adding_a_section_dir(self):
        level_2_node_1 = os.path.join('node_2', 'node_1')
        level_2_node_2 = os.path.join( 'node_2', 'node_2')
        level_2_node_1_examples = os.path.join( 'node_2', 'node_1', 'examples')
        level_2_node_2_examples = os.path.join( 'node_2', 'node_2', 'examples')
        self.tree.add(
            'node_2',
            dirs=['node_1', 'node_2'])
        self.tree.add(
            level_2_node_1,
            dirs=['examples'])
        self.tree.add(
            level_2_node_2,
            dirs=['examples'])
        self.tree.add(
            level_2_node_1_examples,
            files=['example_1.html', 'example_2.html'])
        self.tree.add(
            level_2_node_2_examples,
            files=['example_1.html', 'example_2.html', 'example_3.html'])
        assert self.tree.get('node_2') == {
            'type': 'section',
            'children': {
                'node_1' : {
                    'type': 'pattern',
                    'examples': [
                        'example_1.html',
                        'example_2.html'
                    ]
                },
                'node_2' : {
                    'type': 'pattern',
                    'examples': [
                        'example_1.html',
                        'example_2.html',
                        'example_3.html'
                    ]
                }
            }
        }


class TestStructure(object):
    def setup(self):
        _clean(['test_src', 'test_dst'])

    def teardown(self):
        _clean(['test_src', 'test_dst'])

    def test_folder_structure_created(self):
        os.makedirs('test_src/level_1/level_2')
        open(os.path.join(root, 'test_src/level_1/level_2/index.html'), 'w')
        structure = build.Structure('test_src', 'test_dst')
        structure.create_tree()

        assert os.path.exists('test_dst/level_1/level_2/index.html')
