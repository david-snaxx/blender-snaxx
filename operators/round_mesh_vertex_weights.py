import bpy

class BS_OT_RoundMeshVertexWeights(bpy.types.Operator):
    bl_idname = "bs.round_mesh_vertex_weights"
    bl_label = "Round Mesh Vertex Weights"
    bl_options = {'REGISTER', 'UNDO'}

    # noinspection PyTypeHints
    decimal_places : bpy.props.IntProperty(
        name = "Decimal Places",
        description = "Number of decimal places to round vertex weights to.",
        default = 2,
        min = 0,
        max = 10,
    )

    def execute(self, context):
        for obj in self.get_selected_mesh_objects(context):
            locked_vertex_groups = self.store_locked_vertex_groups(obj)
            self.unlock_locked_vertex_groups(obj)

            for vertex in obj.data.vertices:
                self.quantize_vertex_weights(vertex)

            self.relock_locked_vertex_groups(obj, locked_vertex_groups)
        return { 'FINISHED' }

    @staticmethod
    def get_selected_mesh_objects(context):
        selected = []
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                selected.append(obj)
        return selected

    @staticmethod
    def store_locked_vertex_groups(obj):
        locked_vertex_groups = set()
        for vertex_group in obj.vertex_groups:
            if vertex_group.lock_weight:
                locked_vertex_groups.add(vertex_group)
        return locked_vertex_groups

    @staticmethod
    def unlock_locked_vertex_groups(obj):
        for vertex_group in obj.vertex_groups:
            if vertex_group.lock_weight:
                vertex_group.lock_weight = False

    @staticmethod
    def relock_vertex_groups(obj, locked_vertex_groups):
        for vertex_group in obj.vertex_groups:
            vertex_group.lock_weight = True

    @staticmethod
    def quantize_vertex_weights(self, vertex):
        """Rewrites one vertex's weights so each is a multiple of 10^-decimal_places, and they sum to exactly 1.0."""
        units_per_whole = 10 ** self.decimal_places

        assignments = list(vertex.groups)
        weight_total = sum(assignment.weight for assignment in assignments)
        if weight_total <= 0:
            return

        # each group's share of this vertex's total weight, summing to 1.0
        proportions = [assignment.weight / weight_total for assignment in assignments]
        allocated_units = self.allocate_units_largest_remainder(proportions, units_per_whole)

        for assignment, unit_count in zip(assignments, allocated_units):
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

def register():
    bpy.types.Secne.bs_decimal_places = bpy.props.IntProperty(
        name = "Decimal Places",
        description = "Number of decimal places to round vertex weights to.",
        default = 2,
        min = 0,
        max = 10,
    )
    bpy.utils.register_class(BS_OT_RoundMeshVertexWeights)

def unregister():
    bpy.utils.unregister_class(BS_OT_RoundMeshVertexWeights)

if __name__ == "__main__":
    register()
