import bpy

class BS_OT_CleanVertexGroups(bpy.types.Operator):
    bl_idname = "bs.clean_vertex_groups"
    bl_label = "Clean vertex groups"
    bl_description = "Removes any unweighted or unassigned vertex groups from the selected mesh."
    bl_options = {'REGISTER', 'UNDO'}

    # noinspection PyTypeHints
    require_armature: bpy.props.BoolProperty(
        name = "Require armature",
        description = "Only performs cleaning operations if the selected mesh has an armature.",
        default = True,
    )

    # noinspection PyTypeHints
    remove_unweighted : bpy.props.BoolProperty(
        name = "Unweighted",
        description = "Remove vertex groups with no vertex weights from all selected MESH objects.",
        default = True,
    )

    # noinspection PyTypeHints
    force_remove_unassigned_without_armature: bpy.props.BoolProperty(
        name = "Unassigned without armature/bone assignment",
        description = "When Unassigned is enabled and a mesh has no detected armature, remove ALL of its "
                    "vertex groups instead of skipping the check. There are no bones to match against, "
                    "so every group counts as unassigned. This will remove groups that still have weights "
                    "assigned — use with caution.",
        default = False,
    )

    # noinspection PyTypeHints
    remove_unassigned : bpy.props.BoolProperty(
        name = "Unassigned",
        description = "Remove vertex groups that are not assigned to any bones from all selected MESH objects.",
        default = False,
    )

    def execute(self, context):
        selected = context.selected_objects
        selected_meshes = []
        for obj in selected:
            if obj.type == 'MESH':
                selected_meshes.append(obj)

        for obj in selected_meshes:
            mesh = obj.data
            armature = self.get_mesh_armature(obj)

            if self.require_armature and armature is None:
                self.report({'WARNING'}, f"'{obj.name}' has no armature; skipping (Require Armature is enabled)")
                continue

            # reset per object, these indices are only meaningful within
            # this object's own vertex_groups list, not across objects
            used_vertex_groups_indices = set()
            if self.remove_unweighted:
                for vertex in mesh.vertices:
                    # find every vertex group that is touched by at least one vertex of the mesh
                    # an "unused" vertex group has no vertex weight assignments
                    for assignment in vertex.groups:
                        used_vertex_groups_indices.add(assignment.group)

            armature_group_indices = set()
            check_unassigned = self.remove_unassigned
            if self.remove_unassigned:
                armature_object = self.get_mesh_armature(obj)
                if armature_object is None:
                    if self.force_remove_unassigned_without_armature:
                        # no bones exist to match against, so every vertex group
                        # on this mesh counts as unassigned by definition
                        self.report({'WARNING'}, f"'{obj.name}' has no armature; treating all vertex groups as unassigned")
                        # armature_group_indices stays empty on purpose
                    else:
                        self.report({'WARNING'}, f"'{obj.name}' has no armature; skipping unassigned check")
                        check_unassigned = False
                else:
                    bone_names = armature.data.bones.keys()
                    for vertex_group in obj.vertex_groups:
                        if vertex_group.name in bone_names:
                            armature_group_indices.add(vertex_group.index)

                    for vertex_group in obj.vertex_groups:
                        if vertex_group.name in bone_names:
                            armature_group_indices.add(vertex_group.index)

            # start reversed to avoid shifting index issues when items are removed
            # a group is removed if it fails ANY currently-enabled criterion below
            for vertex_group in reversed(obj.vertex_groups):
                should_remove = False

                if self.remove_unweighted:
                    if vertex_group.index not in used_vertex_groups_indices:
                        should_remove = True

                if check_unassigned:
                    if vertex_group.index not in armature_group_indices:
                        should_remove = True

                if should_remove:
                    obj.vertex_groups.remove(vertex_group)

        self.report({'INFO'}, f"Finished cleaning vertex groups")
        return { 'FINISHED' }

    @staticmethod
    def get_mesh_armature(mesh_object):
        if mesh_object.parent and mesh_object.parent.type == 'ARMATURE':
            return mesh_object.parent
        for modifier in mesh_object.modifiers:
            if modifier.type == 'ARMATURE' and modifier.object:
                return modifier.object
        return None

def register():
    bpy.types.Scene.bs_require_armature = bpy.props.BoolProperty(
        name = "Require armature",
        default = True,
    )
    bpy.types.Scene.bs_remove_unweighted = bpy.props.BoolProperty(
        name = "Unweighted",
        default = True,
    )
    bpy.types.Scene.bs_force_remove_unassigned_without_armature = bpy.props.BoolProperty(
        name = "Unassigned without armature/bone assignment",
        default = True,
    )
    bpy.types.Scene.bs_remove_unassigned = bpy.props.BoolProperty(
        name = "Unassigned with armature/bone assignment",
        default = False,
    )
    bpy.utils.register_class(BS_OT_CleanVertexGroups)

def unregister():
    del bpy.types.Scene.bs_require_armature
    del bpy.types.Scene.bs_remove_unweighted
    del bpy.types.Scene.bs_force_remove_unassigned_without_armature
    del bpy.types.Scene.bs_remove_unassigned
    bpy.utils.unregister_class(BS_OT_CleanVertexGroups)
