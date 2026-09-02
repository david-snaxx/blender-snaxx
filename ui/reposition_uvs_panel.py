import bpy

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
            preview_panel.label(text="WIP", icon='INFO')
