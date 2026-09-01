import bpy
from ..utils.getters import (get_selected_mesh_objects,
                           get_mesh_armature)

class BS_OT_CleanUnusedVertexGroups(bpy.types.Operator):
    bl_idname = "bs.clean_unused_vertex_groups"
    bl_label = "Clean unused vertex groups"
    bl_options = {"REGISTER", "UNDO"}

    # noinspection PyTypeHints
    remove_unweighted : bpy.props.BoolProperty(
        name = "Unweighted Groups",
        description = "Remove vertex groups in which no vertex within the group has weight data from all selected "
                      "mesh objects.",
        default = True,
    )
    # noinspection PyTypeHints
    remove_unassigned : bpy.props.BoolProperty(
        name = "Unassigned",
        description = "Remove vertex groups that are not assigned to any bones from all selected mesh objects. "
                      "Assigned to bones means the name of the vertex group matches the name of a bone of an attached "
                      "armature.",
        default = False,
    )

    def execute(self, context):
        for obj in get_selected_mesh_objects(context):
            mesh = obj.data

            assigned_weights_vertex_group_indices = set()
            if self.remove_unweighted:
                for vertex in mesh.vertices:
                    # find vertex groups with at least one vertex weight assignment
                    for assignment in vertex.groups:
                        assigned_weights_vertex_group_indices.add(assignment.group)

            should_check_unassigned = self.remove_unassigned
            assigned_armature_bone_vertex_group_indices = set()
            if self.remove_unassigned:
                armature = get_mesh_armature(obj)
                if armature is None:
                    self.report({"WARNING"}, f"{obj.name} does not have an armature; skipping unassigned removal")
                    should_check_unassigned = False
                else:
                    # find vertex groups whose name matches a bone of the armature
                    bone_names = armature.data.bones.keys()
                    for vertex_group in obj.vertex_groups:
                        if vertex_group.name in bone_names:
                            assigned_armature_bone_vertex_group_indices.add(vertex_group.index)

            # start reversed to avoid shifting index issues when items are removed
            # a group is removed if it fails ANY currently-enabled criterion below
            for vertex_group in reversed(obj.vertex_groups):
                should_remove = False

                if self.remove_unweighted:
                    if vertex_group.index not in assigned_weights_vertex_group_indices:
                        should_remove = True

                if should_check_unassigned:
                    if vertex_group.index not in assigned_armature_bone_vertex_group_indices:
                        should_remove = True

                if should_remove:
                    obj.vertex_groups.remove(vertex_group)
        self.report({"INFO"}, "Finished cleaning vertex groups")
        return {"FINISHED"}

def register():
    bpy.types.Scene.bs_remove_unweighted = bpy.props.BoolProperty(
        name = "Unweighted",
        description = "Remove vertex groups with no vertex weights from all selected mesh objects.",
        default = True,
    )
    bpy.types.Scene.bs_remove_unassigned = bpy.props.BoolProperty(
        name = "Unassigned",
        description = "Remove vertex groups that are not assigned to any bones from all selected mesh objects.",
        default = False,
    )
    bpy.utils.register_class(BS_OT_CleanUnusedVertexGroups)

def unregister():
    del bpy.types.Scene.bs_remove_unweighted
    del bpy.types.Scene.bs_remove_unassigned
    bpy.utils.unregister_class(BS_OT_CleanUnusedVertexGroups)

if __name__ == "__main__":
    register()
