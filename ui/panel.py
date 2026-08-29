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
        self.draw_clean_vertex_groups(context, layout, scene)
        self.draw_rename_child_to_match_parent(context, layout, scene)

    def draw_clean_vertex_groups(self, context, layout, scene):
        box = layout.box()
        box.label(text = "Clean vertex groups")
        # options
        col = box.column()
        col.prop(scene, "bs_require_armature")
        col.prop(scene, "bs_remove_unweighted")
        col.prop(scene, "bs_force_remove_unassigned_without_armature")
        col.prop(scene, "bs_remove_unassigned")
        # runner
        op = box.operator("bs.clean_vertex_groups", text="Clean vertex groups")
        op.require_armature = scene.bs_require_armature
        op.remove_unweighted = scene.bs_remove_unweighted
        op.force_remove_unassigned_without_armature = scene.bs_force_remove_unassigned_without_armature
        op.remove_unassigned = scene.bs_remove_unassigned

    def draw_rename_child_to_match_parent(self, context, layout, scene):
        box = layout.box()
        box.label(text="Rename child to match parent")
        # options
        col = box.column()
        col.prop(scene, "bs_prefix")
        col.prop(scene, "bs_suffix")
        # preview
        parent_child_dict = (rename_child_to_match_parent
                             .BS_OT_RenameChildToMatchParent
                             .get_parent_child_grouping(context.selected_objects))
        valid, conflicting = (rename_child_to_match_parent
                              .BS_OT_RenameChildToMatchParent
                              .split_parent_child_groups_to_valid_and_conflicting(parent_child_dict))
        if not valid and not conflicting:
            box.label(text="Nothing selected", icon="INFO")

        if valid:
            sub = box.box()
            sub.label(text=f"Found {len(valid)} objects:", icon="CHECKMARK")
            for parent, child in valid.items():
                row = sub.row()
                row.label(text=f"{child.name} ...->... {scene.bs_prefix}{parent.name}{scene.bs_suffix}")

        if conflicting:
            sub = box.box()
            sub.label(text=f"Conflicting selections (these objects will not be renamed):", icon="ERROR")
            for parent, children in conflicting.items():
                row = sub.row()
                entry_text = ""
                for child in children:
                    entry_text += f"{child.name}, "
                entry_text = entry_text[:-2]
                parent_label = ""
                if parent is None:
                    parent_label = "(no parent)"
                else:
                    parent_label = f"{parent.name}"
                entry_text += f" ...share parent... {parent_label}"
                row.label(text=entry_text)
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
