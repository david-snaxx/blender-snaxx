import bpy

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
        preview_header, preview_panel = panel.panel("bs_shift_uvs_preview_panel", default_closed=True)
        preview_header.label(text="Preview")
        if preview_panel:
            preview_panel.label(text="WIP", icon='INFO')
