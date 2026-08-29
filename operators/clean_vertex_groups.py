import bpy

class BS_OT_CleanVertexGroups(bpy.types.Operator):
    bl_idname = "bs.clean_unused_vertex_groups"
    bl_label = "Clean vertex groups"
    bl_description = "Removes any unweighted or unassigned vertex groups from the selected mesh."
    bl_options = {'REGISTER', 'UNDO'}

    # noinspection PyTypeHints
    remove_unweighted : bpy.props.BoolProperty(
        name = "Unweighted Groups",
        description = "Remove vertex groups with no vertex weights from all selected MESH objects.",
        default = True,
    )

    # noinspection PyTypeHints
    remove_unassigned : bpy.props.BoolProperty(
        name = "Unassigned",
        description = "Remove vertex groups that are not assigned to any bones from all selected MESH objects.",
        default = False,
    )

def register():
    bpy.types.Scene.bs_remove_unweighted = bpy.props.BoolProperty(
        name = "Unweighted Groups",
        default = True,
    )
    bpy.types.Scene.bs_remove_unassigned = bpy.props.BoolProperty(
        name = "Unassigned",
        default = False,
    )
    bpy.utils.register_class(BS_OT_CleanVertexGroups)

def unregister():
    del bpy.types.Scene.bs_remove_unweighted
    del bpy.types.Scene.bs_remove_unassigned
    bpy.utils.unregister_class(BS_OT_CleanVertexGroups)
