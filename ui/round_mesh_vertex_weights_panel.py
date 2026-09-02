import bpy
from ..operators import (round_mesh_vertex_weights)

def draw_round_mesh_vertex_weights(context, layout, scene):
    header, panel = layout.panel("bs_round_mesh_vertex_weights", default_closed = False)
    header.label(text = "Round mesh vertex weights", icon = "GROUP_VERTEX")
    if panel:
        panel.prop(scene, "bs_include_locked_groups")
        panel.prop(scene, "bs_decimal_places")
        op = panel.operator("bs.round_mesh_vertex_weights", text="Round mesh vertex weights")
        op.include_locked_groups = scene.bs_include_locked_groups
        op.decimal_places = scene.bs_decimal_places
        # preview
        preview_box = panel.box()
        preview_header, preview_panel = preview_box.panel("bs_round_mesh_vertex_weights_preview", default_closed = True)
        preview_header.label(text="Preview")
        if preview_panel:
            affected_selected, affected_locked_selected = (round_mesh_vertex_weights
                                                           .BS_OT_RoundMeshVertexWeights
                                                           .get_affected_mesh_objects(context))
            if not affected_selected and not affected_locked_selected:
                preview_panel.label(text="No valid objects selected", icon="INFO")
            if affected_selected:
                sub = preview_panel.box()
                sub.label(text=f"Found {len(affected_selected)} candidate mesh objects:", icon="CHECKMARK")
                for obj in affected_selected:
                    row = sub.row()
                    row.label(text=obj.name)
            if affected_locked_selected:
                sub = preview_panel.box()
                sub.label(text=f"Found {len(affected_locked_selected)} candidate mesh objects with locked groups:",
                          icon="INFO")
                sub.label(text="Include locked groups must be toggled to affect all vertex groups")
                for obj in affected_locked_selected:
                    row = sub.row()
                    row.label(text=obj.name)
