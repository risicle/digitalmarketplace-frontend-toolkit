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
