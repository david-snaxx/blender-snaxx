import bpy
from ..utils.getters import get_selected_mesh_objects
from ..operators.reposition_uvs import get_current_uv_tile_coords

def draw_reposition_uvs(context, layout, scene):
    header, panel = layout.panel("bs_reposition_uvs_panel", default_closed=False)
    header.label(text="Reposition UVs", icon='UV')
    if panel:
        panel.use_property_split = True
        panel.use_property_decorate = False
        col = panel.column()
        col.prop(scene, "bs_reposition_x")
        col.prop(scene, "bs_reposition_y")
        col.prop(scene, "bs_reposition_target")
        panel.separator()
        row = panel.row()
        row.alignment = 'CENTER'
        row.scale_y = 1.4
        op = row.operator("bs.reposition_uvs", text="Reposition UVs", icon="GHOST_ENABLED")
        op.reposition_x = scene.bs_reposition_x
        op.reposition_y = scene.bs_reposition_y
        op.reposition_target = scene.bs_reposition_target
        # preview
        preview_header, preview_panel = panel.panel("bs_reposition_uvs_preview_panel", default_closed=True)
        preview_header.label(text="Preview")
        if preview_panel:
            selected_mesh_objects = get_selected_mesh_objects(context)
            if not selected_mesh_objects:
                preview_panel.label(text="No meshes selected", icon="INFO")
            else:
                sub = preview_panel.box()
                target_u, target_v = scene.bs_reposition_x, scene.bs_reposition_y
                for obj in selected_mesh_objects:
                    row = sub.row()
                    if not obj.data.uv_layers:
                        row.label(text=f"{obj.name}: no UV maps", icon="ERROR")
                        continue
                    current_u, current_v = get_current_uv_tile_coords(obj)
                    row.label(text=f"{obj.name}: ({current_u}, {current_v}) → ({target_u}, {target_v})")
