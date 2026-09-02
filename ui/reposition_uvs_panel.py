import bpy

def draw_reposition_uvs(context, layout, scene):
    header, panel = layout.panel("bs_reposition_uvs_panel", default_closed=False)
    header.label(text="Reposition UVs", icon='UV')
    if panel:
        panel.prop(scene, "bs_reposition_x")
        panel.prop(scene, "bs_reposition_y")
        panel.prop(scene, "bs_reposition_target")
        op = panel.operator("bs.reposition_uvs", text="Reposition UVs")
        op.move_x = scene.bs_reposition_x
        op.move_y = scene.bs_reposition_y
        op.move_target = scene.bs_reposition_target
        preview_box = panel.box()
        preview_header, preview_panel = preview_box.panel("bs_reposition_uvs_preview_panel", default_closed=True)
        preview_header.label(text="Preview")
        if preview_panel:
            preview_panel.label(text="WIP", icon='INFO')
