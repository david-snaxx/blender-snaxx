import bpy
from ..utils.getters import get_selected_mesh_objects
from ..operators.shift_uvs import get_current_uv_tile_coords

def draw_shift_uvs(context, layout, scene):
    header, panel = layout.panel("bs_shift_uvs_panel", default_closed=False)
    header.label(text="Shift UVs", icon='UV')
    if panel:
        panel.use_property_split = True
        panel.use_property_decorate = False
        col = panel.column()
        col.prop(scene, "bs_move_x")
        col.prop(scene, "bs_move_y")
        col.prop(scene, "bs_move_target")
        panel.separator()
        row = panel.row()
        row.alignment = 'CENTER'
        row.scale_y = 1.4
        op = row.operator("bs.shift_uvs", text="Shift UVs", icon="GHOST_ENABLED")
        op.move_x = scene.bs_move_x
        op.move_y = scene.bs_move_y
        op.move_target = scene.bs_move_target
        # preview
        preview_header, preview_panel = panel.panel("bs_shift_uvs_panel_preview", default_closed=True)
        preview_header.label(text="Preview")
        if preview_panel:
            selected_mesh_objects = get_selected_mesh_objects(context)
            if not selected_mesh_objects:
                preview_panel.label(text="No meshes selected", icon="INFO")
            else:
                sub = preview_panel.box()
                for obj in selected_mesh_objects:
                    row = sub.row()
                    if not obj.data.uv_layers:
                        row.label(text=f"{obj.name}: no UV maps", icon="ERROR")
                        continue
                    current_u, current_v = get_current_uv_tile_coords(obj)
                    target_u = current_u + scene.bs_move_x
                    target_v = current_v + scene.bs_move_y
                    row.label(text=f"{obj.name}: ({current_u}, {current_v}) → ({target_u}, {target_v})")
