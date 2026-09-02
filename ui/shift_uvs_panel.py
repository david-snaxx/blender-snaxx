import bpy

def draw_shift_uvs(context, layout, scene):
    header, panel = layout.panel("bs_shift_uvs_panel", default_closed=False)
    header.label(text="Shift UVs", icon='UV')
    if panel:
        panel.prop(scene, "bs_move_x")
        panel.prop(scene, "bs_move_y")
        panel.prop(scene, "bs_move_target")
        op = panel.operator("bs.shift_uvs", text="Shift UVs")
        op.move_x = scene.bs_move_x
        op.move_y = scene.bs_move_y
        op.move_target = scene.bs_move_target
        # preview
        preview_header, preview_panel = panel.panel("bs_shift_uvs_preview_panel", default_closed=True)
        preview_header.label(text="Preview")
        if preview_panel:
            preview_panel.label(text="WIP", icon='INFO')
