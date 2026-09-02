import bpy

def draw_shift_uvs(context, layout, scene):
    header, panel = layout.panel("bs_shift_uvs_panel", default_closed=False)
    header.label(text="Shift UVs", icon='UV')
    if panel:
        panel.prop(scene, "bs_move_x")
        panel.prop(scene, "bs_move_y")
        panel.prop(scene, "bs_move_active_uv_map")
        panel.prop(scene, "bs_move_all_uv_maps")
        op = panel.operator("bs.shift_uvs", text="Shift UVs")
        op.move_x = scene.bs_move_x
        op.move_y = scene.bs_move_y
        op.move_active_uv_map = scene.bs_move_active_uv_map
        op.move_all_uv_maps = scene.bs_move_all_uv_maps
        # preview
        preview_box = panel.box()
        preview_header, preview_panel = preview_box.panel("bs_shift_uvs_preview_panel", default_closed=True)
        preview_header.label(text="Preview", icon='INFO')
        if preview_panel:
            preview_panel.label(text="WIP", icon='INFO')
