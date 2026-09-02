import bpy
from ..utils.getters import (get_selected_mesh_objects)


class SB_OT_QuantizeVertexWeights(bpy.types.Operator):
    """Quantize vertex weights of all selected meshes to a fixed number of steps"""
    bl_idname = "bs.quantize_selected_weights"
    bl_label = "Quantize Selected Weights"
    bl_options = {'REGISTER', 'UNDO'}

    # noinspection PyTypeHints
    quantize_steps: bpy.props.IntProperty(
        name="Steps",
        description="Discrete steps to quantize into "
                    "(255 matches 8-bit normalized byte weights)",
        default=255,
        min=1,
        max=1024,
    )

    def execute(self, context):
        # storing state for later
        original_active_object = context.view_layer.objects.active
        original_mode = context.view_layer.objects.active.mode if original_active_object else 'OBJECT'

        # must be in OBJECT mode to swap between all selected objects
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # iteratively change the active object to each mesh and run the quantize function
        selected_mesh_objects = get_selected_mesh_objects(context)
        if not selected_mesh_objects:
            self.report({'ERROR'}, "No meshes selected")
            return {'CANCELLED'}

        processed = 0
        skipped = []
        try:
            for selected_mesh in selected_mesh_objects:
                # skip any with no vertex groups
                if not selected_mesh.vertex_groups:
                    skipped.append(selected_mesh.name)
                    continue
                context.view_layer.objects.active = selected_mesh
                bpy.ops.object.vertex_group_quantize(group_select_mode='ALL', steps=self.steps)
                processed += 1
        finally:
            # restore prior state
            context.view_layer.objects.active = original_active_object
            if original_active_object and original_active_object.mode != original_mode:
                bpy.ops.object.mode_set(mode=original_mode)

        if skipped:
            self.report({'WARNING'},
                        f"Quantized {processed} mesh(es); skipped {len(skipped)} with no vertex groups: {', '.join(skipped)}")
        else:
            self.report({'INFO'}, f"Quantized {processed} mesh(es)")
        return {'FINISHED'}

def register():
    bpy.types.Scene.bs_quantize_steps = bpy.props.IntProperty(
        name="Steps",
        description="Discrete steps to quantize into "
                    "(255 matches 8-bit normalized byte weights)",
        default=255,
        min=1,
        max=1024,
    )
    bpy.utils.register_class(SB_OT_QuantizeVertexWeights)


def unregister():
    del bpy.types.Scene.sb_quantize_steps
    bpy.utils.unregister_class(SB_OT_QuantizeVertexWeights)


if __name__ == "__main__":
    register()
