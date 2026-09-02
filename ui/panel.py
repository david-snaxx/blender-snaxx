import bpy
from ..operators import (rename_child_to_match_parent,
                         round_mesh_vertex_weights)
from .clean_unused_vertex_groups_panel import (draw_clean_unused_vertex_groups)
from .rename_child_to_match_parent_panel import (draw_rename_child_to_match_parent)
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
        self.round_mesh_vertex_weights(context, layout, scene)
        draw_shift_uvs(context, layout, scene)


    def round_mesh_vertex_weights(self, context, layout, scene):
        box = layout.box()
        box.label(text="Round mesh vertex weights")
        # options
        col = box.column()
        col.prop(scene, "bs_include_locked_groups")
        col.prop(scene, "bs_decimal_places")
        # preview
        affected_selected, affected_locked_selected = (round_mesh_vertex_weights
                                                       .BS_OT_RoundMeshVertexWeights
                                                       .get_affected_mesh_objects(context))
        if not affected_selected and not affected_locked_selected:
            box.label(text="No valid objects selected", icon="INFO")
        if affected_selected:
            sub = box.box()
            sub.label(text = f"Found {len(affected_selected)} candidate mesh objects:", icon = "CHECKMARK")
            for obj in affected_selected:
                row = sub.row()
                row.label(text = obj.name)
        if affected_locked_selected:
            sub = box.box()
            sub.label(text = f"Found {len(affected_locked_selected)} candidate mesh objects with locked groups:", icon = "INFO")
            sub.label(text = "Include locked groups must be toggled to affect all vertex groups")
            for obj in affected_locked_selected:
                row = sub.row()
                row.label(text = obj.name)
        # runner
        op = box.operator("bs.round_mesh_vertex_weights", text="Round mesh vertex weights")
        op.include_locked_groups = scene.bs_include_locked_groups
        op.decimal_places = scene.bs_decimal_places



def register():
    bpy.utils.register_class(BS_PT_Panel)

def unregister():
    bpy.utils.unregister_class(BS_PT_Panel)

if __name__ == "__main__":
    register()
