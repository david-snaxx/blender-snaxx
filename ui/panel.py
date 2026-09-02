import bpy
from .clean_unused_vertex_groups_panel import (draw_clean_unused_vertex_groups)
from .rename_child_to_match_parent_panel import (draw_rename_child_to_match_parent)
from .round_mesh_vertex_weights_panel import (draw_round_mesh_vertex_weights)
from .shift_uvs_panel import (draw_shift_uvs)

class BS_PT_Panel(bpy.types.Panel):
    bl_idname = "bs.panel"
    bl_label = "BlenderSnaxx"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BlenderSnaxx"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        draw_clean_unused_vertex_groups(context, layout, scene)
        draw_rename_child_to_match_parent(context, layout, scene)
        draw_round_mesh_vertex_weights(context, layout, scene)
        draw_shift_uvs(context, layout, scene)





def register():
    bpy.utils.register_class(BS_PT_Panel)

def unregister():
    bpy.utils.unregister_class(BS_PT_Panel)

if __name__ == "__main__":
    register()
