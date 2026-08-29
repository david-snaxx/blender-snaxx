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
        meshes = self.get_selected_mesh_objects(context)
        for obj in meshes:
            armature = self.get_mesh_armature(obj)

            if self.require_armature and armature is None:
                self.report({"WARNING"}, f"{obj.name} has no armature; skipping (Require Armature is enabled)")
                continue

            check_unweighted_groups = self.remove_unweighted
            assigned_vertex_groups_indices = set()
            if check_unweighted_groups:
                assigned_vertex_groups_indices = self.get_assigned_vertex_group_indices(obj.data) #.data since we know this is a mesh

            check_unassigned_groups, assigned_armature_vertex_groups_indices = self.get_unassigned_check_state(obj, armature)

            # start reversed to avoid shifting index issues when items are removed
            for vertex_group in reversed(obj.vertex_groups):
                if self.should_remove_vertex_group(
                        vertex_group,
                        check_unweighted_groups, assigned_vertex_groups_indices,
                        check_unassigned_groups, assigned_armature_vertex_groups_indices,
                ):
                    obj.vertex_groups.remove(vertex_group)
        self.report({'INFO'}, f"Finished cleaning vertex groups")
        return { 'FINISHED' }

    @staticmethod
    def get_selected_mesh_objects(context):
        selected = context.selected_objects
        selected_meshes = []
        for obj in selected:
            if obj.type == 'MESH':
                selected_meshes.append(obj)
        return selected_meshes

    @staticmethod
    def get_mesh_armature(mesh):
        """Returns the armature of the given mesh, or None if no armature exists"""
        if mesh.parent and mesh.parent.type == 'ARMATURE':
            return mesh.parent
        for modifier in mesh.modifiers:
            if modifier.type == 'ARMATURE' and modifier.object:
                return modifier.object
        return None

    @staticmethod
    def get_assigned_vertex_group_indices(mesh):
        """Returns the indices of a mesh's vertex groups that have at least one vertex assigned in the group"""
        used_indices = set()
        for vertex in mesh.vertices:
            for assignment in vertex.groups:
                used_indices.add(assignment.group)
        return used_indices

    @staticmethod
    def get_armature_bone_assigned_vertex_group_indices(obj, armature):
        """Returns the indices of a mesh's vertex groups whose name matches a bone on the given armature"""
        bone_names = armature.data.bones.keys()
        used_indices = set()
        for vertex_group in obj.vertex_groups:
            if vertex_group.name in bone_names:
                used_indices.add(vertex_group.index)
        return used_indices

    @staticmethod
    def should_remove_vertex_group(vertex_group, check_unweighted, assigned_vertex_group_indices, check_unassigned, armature_assigned_vertex_group_indices):
        if check_unweighted and vertex_group.index not in assigned_vertex_group_indices:
            return True
        if check_unassigned and vertex_group.index not in armature_assigned_vertex_group_indices:
            return True
        return False

    def get_unassigned_check_state(self, obj, armature):
        """
        Decides whether the unassigned (bone-name) check should run for this object,
        and which vertex group indices count as bone-matched if it does.

        Returns a (check_unassigned, armature_group_indices) tuple.
        """
        if not self.remove_unassigned:
            return False, set()

        if armature is None:
            if self.force_remove_unassigned_without_armature:
                # no bones exist to match against, so every vertex group
                # on this mesh counts as unassigned by definition
                self.report({'WARNING'}, f"'{obj.name}' has no armature; treating all vertex groups as unassigned")
                return True, set()
            else:
                self.report({'WARNING'}, f"'{obj.name}' has no armature; skipping unassigned check")
                return False, set()

        return True, self.get_armature_bone_assigned_vertex_group_indices(obj, armature)

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
