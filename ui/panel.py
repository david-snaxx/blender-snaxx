import bpy
from ..operators import (rename_child_to_match_parent)

class BS_PT_Panel(bpy.types.Panel):
    bl_idname = "bs.panel"
    bl_idname = "BS_PT_Panel"
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
        col.prop(scene, "sb_prefix")
        col.prop(scene, "sb_suffix")
        # runner
        op = box.operator("sb.rename_child_to_match_parent", text="Rename child to match parent")
        op.suffix = scene.sb_suffix
        op.prefix = scene.sb_prefix
