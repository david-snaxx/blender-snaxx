import bpy
from ..utils.getters import (get_selected_mesh_objects,
                           get_mesh_armature)
from ..operators import (clean_unused_vertex_groups,
                         rename_child_to_match_parent,
                         round_mesh_vertex_weights)

class BS_PT_Panel(bpy.types.Panel):
    bl_idname = "bs.panel"
    bl_label = "BlenderSnaxx"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BlenderSnaxx"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        self.draw_clean_unusued_vertex_groups(context, layout, scene)
        self.draw_rename_child_to_match_parent(context, layout, scene)
        self.round_mesh_vertex_weights(context, layout, scene)
        self.draw_shift_uvs(context, layout, scene)

    def draw_clean_unusued_vertex_groups(self, context, layout, scene):
        box = layout.box()
        box.label(text = "Clean unused vertex groups")
        # options
        col = box.column()
        col.prop(scene, "bs_remove_unweighted")
        col.prop(scene, "bs_remove_unassigned")
        # preview
        selected_mesh_objects = get_selected_mesh_objects(context)
        has_armature = set()
        no_armature = set()
        for obj in selected_mesh_objects:
            armature = get_mesh_armature(obj)
            if armature is not None:
                has_armature.add(obj)
            else:
                no_armature.add(obj)
        if not has_armature and not no_armature:
            box.label(text="No valid objects selected", icon="INFO")
        if has_armature:
            sub = box.box()
            sub.label(text = f"Found {len(has_armature)} mesh objects with armature:", icon = "CHECKMARK")
            for obj in has_armature:
                row = sub.row()
                row.label(text = obj.name)
        if no_armature:
            sub = box.box()
            sub.label(text = f"Found {len(no_armature)} mesh objects with no armature:", icon = "ERROR")
            sub.label(text = "unassigned clean operation will not run on these objects")
            for obj in no_armature:
                row = sub.row()
                row.label(text = obj.name)
        # runner
        op = box.operator("bs.clean_unused_vertex_groups", text = "Clean unused vertex groups")
        op.remove_unweighted = scene.bs_remove_unweighted
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
            box.label(text="No valid objects selected", icon="INFO")

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

    def round_mesh_vertex_weights(self, context, layout, scene):
        box = layout.box()
        box.label(text="Round mesh vertex weights")
        # options
        col = box.column()
        col.prop(scene, "bs_include_locked_groups")
        col.prop(scene, "bs_decimal_places")
        # preview
        affected_selected, affected_locked_selected = (round_mesh_vertex_weights
                                                       .BS_OT_RoundMeshVertexWeights
                                                       .get_affected_mesh_objects(context))
        if not affected_selected and not affected_locked_selected:
            box.label(text="No valid objects selected", icon="INFO")
        if affected_selected:
            sub = box.box()
            sub.label(text = f"Found {len(affected_selected)} candidate mesh objects:", icon = "CHECKMARK")
            for obj in affected_selected:
                row = sub.row()
                row.label(text = obj.name)
        if affected_locked_selected:
            sub = box.box()
            sub.label(text = f"Found {len(affected_locked_selected)} candidate mesh objects with locked groups:", icon = "INFO")
            sub.label(text = "Include locked groups must be toggled to affect all vertex groups")
            for obj in affected_locked_selected:
                row = sub.row()
                row.label(text = obj.name)
        # runner
        op = box.operator("bs.round_mesh_vertex_weights", text="Round mesh vertex weights")
        op.include_locked_groups = scene.bs_include_locked_groups
        op.decimal_places = scene.bs_decimal_places

    def draw_shift_uvs(self, context, layout, scene):
        panel = layout.panel
        header, panel = layout.panel("bs_shift_uvs_panel", default_closed = False)
        header.label(text = "Shift UVs", icon = 'UV')
        if panel:
            panel.prop(scene, "bs_uv_x")
            panel.prop(scene, "bs_uv_y")
            panel.operator(scene, "bs_shift_uvs")

def register():
    bpy.utils.register_class(BS_PT_Panel)

def unregister():
    bpy.utils.unregister_class(BS_PT_Panel)

if __name__ == "__main__":
    register()
