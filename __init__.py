bl_info = {
    "name": "BlenderSnaxx",
    "author": "david-snaxx",
    "version": (1, 0),
    "blender": (4, 5, 13),
    "location": "View3D > Sidebar > BlenderSnaxx",
    "description": "A collection of blender convenience tools",
    "category": "Object"
}

from .operators import (rename_child_to_match_parent)
from .ui import (panel)

def register():
    rename_child_to_match_parent.register()
    panel.register()

def unregister():
    rename_child_to_match_parent.unregister()
    panel.unregister()

if __name__ == "__main__":
    register()
