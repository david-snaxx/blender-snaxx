import bpy

class BS_OT_RoundMeshVertexWeights(bpy.types.Operator):
    bl_idname = "bs.round_mesh_vertex_weights"
    bl_label = "Round Mesh Vertex Weights"
    bl_description = ("Rounds the weights of the currently selected meshes to the input number of decimal places."
                      "All weights are then adjusted so the total weight sums to 1.0 with remainder weights prioritized "
                      "to the vertices who lost the most from initial rounding truncation.")
    bl_options = {'REGISTER', 'UNDO'}

    # noinspection PyTypeHints
    decimal_places : bpy.props.IntProperty(
        name = "Decimal Places",
        description = "Number of decimal places to round vertex weights to.",
        default = 2,
        min = 0,
        max = 10,
    )

    # noinspection PyTypeHints
    include_locked_groups : bpy.props.BoolProperty(
        name = "Include Locked Groups",
        description = "Quantize weights in locked vertex groups too. When disabled, locked groups keep "
                      "their current weights and only unlocked groups are adjusted.",
        default = True,
    )

    def execute(self, context):
        for obj in self.get_selected_mesh_objects(context):
            all_indices = self.get_all_vertex_group_indices(obj)
            locked_indices = self.get_locked_vertex_group_indices(obj)
            editable_indices = []
            if self.include_locked_groups:
                editable_indices = all_indices
            else:
                editable_indices = all_indices - locked_indices

            for vertex in obj.data.vertices:
                self.quantize_vertex_weights(vertex, editable_indices)

        return {'FINISHED'}

    @staticmethod
    def get_selected_mesh_objects(context):
        selected = []
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                selected.append(obj)
        return selected

    @staticmethod
    def get_locked_vertex_group_indices(obj):
        locked_vertex_group_indices = set()
        for vertex_group in obj.vertex_groups:
            if vertex_group.lock_weight:
                locked_vertex_group_indices.add(vertex_group.index)
        return locked_vertex_group_indices

    @staticmethod
    def get_all_vertex_group_indices(obj):
        all_vertex_group_indices = set()
        for vertex_group in obj.vertex_groups:
            all_vertex_group_indices.add(vertex_group.index)
        return all_vertex_group_indices

    def quantize_vertex_weights(self, vertex, editable_group_indices):
        units_per_whole = 10 ** self.decimal_places

        editable_assignments = []
        reserved_weight_total = 0.0
        for assignment in vertex.groups:
            if assignment.group in editable_group_indices:
                editable_assignments.append(assignment)
            else:
                reserved_weight_total += assignment.weight

        if not editable_assignments:
            return

        available_units = units_per_whole - round(reserved_weight_total * units_per_whole)
        if available_units <= 0:
            for assignment in editable_assignments:
                assignment.weight = 0.0
            return

        editable_weight_total = sum(a.weight for a in editable_assignments)
        if editable_weight_total <= 0:
            return

        proportions = [a.weight / editable_weight_total for a in editable_assignments]
        allocated_units = self.allocate_units_largest_remainder(proportions, available_units)

        for assignment, unit_count in zip(editable_assignments, allocated_units):
            assignment.weight = round(unit_count / units_per_whole, self.decimal_places)

    @staticmethod
    def allocate_units_largest_remainder(proportions, total_units):
        """
        Divides total_units whole units among proportions (which sum to 1.0), so that
        the returned units sum to exactly total_units.

        Each proportion first takes its floor share. Truncation always leaves some
        units unallocated, so those go one each to whichever entries lost the most
        to truncation (largest remainder method).

        Returns a list of ints parallel to proportions.
        """
        exact_units = [proportion * total_units for proportion in proportions]
        whole_units = [int(units) for units in exact_units]

        unallocated_units = total_units - sum(whole_units)
        if unallocated_units:
            # entry indices ordered by how much each lost to truncation, largest first
            by_remainder = sorted(
                range(len(exact_units)),
                key = lambda i: exact_units[i] - whole_units[i],
                reverse = True,
            )
            for i in by_remainder[:unallocated_units]:
                whole_units[i] += 1

        return whole_units

    @staticmethod
    def get_affected_mesh_objects(context):
        affected = []
        affected_locked = []
        for obj in BS_OT_RoundMeshVertexWeights.get_selected_mesh_objects(context):
            if not obj.vertex_groups:
                continue

            locked_indices = BS_OT_RoundMeshVertexWeights.get_locked_vertex_group_indices(obj)
            has_any_weights = False
            has_editable_weights = False
            for vertex in obj.data.vertices:
                for assignment in vertex.groups:
                    # there are some weights by this point
                    has_any_weights = True
                    if assignment.group not in locked_indices:
                        # this group wasn't locked
                        has_editable_weights = True
                        break
                if has_editable_weights:
                    break

            if has_editable_weights:
                affected.append(obj)
            elif has_any_weights:
                affected_locked.append(obj)
        return affected, affected_locked

def register():
    bpy.types.Scene.bs_decimal_places = bpy.props.IntProperty(
        name = "Decimal Places",
        description = "Number of decimal places to round vertex weights to.",
        default = 2,
        min = 0,
        max = 10,
    )
    bpy.types.Scene.bs_include_locked_groups = bpy.props.BoolProperty(
        name = "Include Locked Groups",
        description = "Quantize weights in locked vertex groups too. When disabled, locked groups keep "
                      "their current weights and only unlocked groups are adjusted.",
        default = True,
    )
    bpy.utils.register_class(BS_OT_RoundMeshVertexWeights)

def unregister():
    del bpy.types.Scene.bs_decimal_places
    del bpy.types.Scene.bs_include_locked_groups
    bpy.utils.unregister_class(BS_OT_RoundMeshVertexWeights)

if __name__ == "__main__":
    register()
