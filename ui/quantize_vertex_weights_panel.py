import bpy
from ..utils.getters import get_selected_mesh_objects

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
            selected_mesh_objects = get_selected_mesh_objects(context)
            if not selected_mesh_objects:
                preview_panel.label(text="No meshes selected", icon="INFO")
            else:
                increment = 1.0 / scene.bs_quantize_steps if scene.bs_quantize_steps else 0.0
                preview_panel.label(text=f"Weight increment at {scene.bs_quantize_steps} steps: {increment:.5f}")
                #example: if steps: 0.5, then possible weights are 0.5 apart, so 0.05, 0.010, 0.015... until 0.0/1.0
                preview_panel.label(text="This is the gap between each possible weight value after quantization.")
                preview_panel.label(text="Weights closer together than this will become identical.")

                sub = preview_panel.box()
                for obj in selected_mesh_objects:
                    row = sub.row()
                    if not obj.vertex_groups:
                        row.label(text=f"{obj.name}: no vertex groups, skipping", icon="ERROR")
                    else:
                        row.label(text=f"{obj.name}: {len(obj.vertex_groups)} group(s) will be quantized", icon="CHECKMARK")