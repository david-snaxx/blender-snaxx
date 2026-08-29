bl_info = {
    "name": "BlenderSnaxx",
    "author": "david-snaxx",
    "version": (1, 0),
    "blender": (4, 5, 13),
    "location": "View3D > Sidebar > BlenderSnaxx",
    "description": "A collection of blender convenience tools",
    "category": "Object"
}

from .operators import (clean_unused_vertex_groups,
                        rename_child_to_match_parent,
                        round_mesh_vertex_weights)
from .ui import (panel)

def register():
    clean_unused_vertex_groups.register()
    rename_child_to_match_parent.register()
    round_mesh_vertex_weights.register()
    panel.register()

def unregister():
    clean_unused_vertex_groups.unregister()
    rename_child_to_match_parent.unregister()
    round_mesh_vertex_weights.unregister()
    panel.unregister()

if __name__ == "__main__":
    register()
