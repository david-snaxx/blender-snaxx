import bpy
from ..operators import (rename_child_to_match_parent)

class BS_PT_Panel(bpy.types.Panel):
    bl_idname = "bs.panel"
    bl_label = "BlenderSnaxx"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BlenderSnaxx"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        self.draw_rename_child_to_match_parent(context, layout, scene)

    def draw_rename_child_to_match_parent(self, context, layout, scene):
        box = layout.box()
        box.label(text="Rename child to match parent")
        # options
        col = box.column()
        col.prop(scene, "bs_prefix")
        col.prop(scene, "bs_suffix")
        # runner
        op = box.operator("bs.rename_child_to_match_parent", text="Rename child to match parent")
        op.suffix = scene.bs_suffix
        op.prefix = scene.bs_prefix

def register():
    bpy.utils.register_class(BS_PT_Panel)

def unregister():
    bpy.utils.unregister_class(BS_PT_Panel)

if __name__ == "__main__":
    register()
