import bpy

def draw_quantize_vertex_weights(context, layout, scene):
    header, panel = layout.panel("bs_quantize_selected_weights", default_closed=False)
    header.label(text="Quantize Selected Weights", icon='GROUP_VERTEX')
    if panel:
        panel.use_property_split = True
        panel.use_property_decorate = False
        col = panel.column()
        col.prop(scene, "bs_quantize_steps")
        panel.separator()
        row = panel.row()
        row.alignment = 'CENTER'
        row.scale_y = 1.4
        op = row.operator("bs.quantize_selected_weights", text="Quantize Selected Weights", icon="GHOST_ENABLED")
        op.quantize_steps = scene.bs_quantize_steps
        # preview
        preview_header, preview_panel = panel.panel("bs_quantize_selected_weights_panel_preview", default_closed=True)
        preview_header.label(text="Preview")
        if preview_panel:
            preview_panel.label(text="WIP", icon='INFO')