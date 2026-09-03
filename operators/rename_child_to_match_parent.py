import bpy

class BS_OT_RenameChildToMatchParent(bpy.types.Operator):
    bl_idname = "bs.rename_child_to_match_parent"
    bl_label = "Rename Child to Match Parent Object"
    bl_description = ("Renames the selected child object to match its parent object's name with an optional prefix"
                      "and suffix.")
    bl_options = {'REGISTER', 'UNDO'}

    # noinspection PyTypeHints
    prefix: bpy.props.StringProperty(
        name = "Prefix",
        description = "Text that will be appended to the start of the new name.",
        default = "",
    )

    # noinspection PyTypeHints
    suffix: bpy.props.StringProperty(
        name = "Suffix",
        description = "Text that will be appended to the end of the new name.",
        default = "",
    )

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) == 0:
            self.report({'ERROR'}, "No objects selected")
            return {'FINISHED'}

        parent_child_dict = self.get_parent_child_grouping(selected)
        valid, conflicting = self.split_parent_child_groups_to_valid_and_conflicting(parent_child_dict)

        if (len(valid) == 0 and len(conflicting) == 0):
            self.report({'ERROR'}, "No valid objects found in selection")
            return {'CANCELLED'}
        if (len(valid) == 0 and len(conflicting) > 0):
            self.report({'ERROR'}, "No single child-parent pairings found in selection.")
            return {'CANCELLED'}

        for parent, child in valid.items():
            child.name = f"{self.prefix}{parent.name}{self.suffix}"

        self.report({'INFO'}, f"Successfully renamed {len(valid)} child object")
        return {'FINISHED'}

    @staticmethod
    def get_parent_child_grouping(selected):
        parent_child_dict = {}
        for obj in selected:
            if obj.parent not in parent_child_dict:
                parent_child_dict[obj.parent] = []
            parent_child_dict[obj.parent].append(obj)
        return parent_child_dict

    @staticmethod
    def split_parent_child_groups_to_valid_and_conflicting(parent_child_dict):
        valid = {}
        conflicting = {}
        for parent, children in parent_child_dict.items():
            if (len(children) > 1 or parent is None):
                conflicting[parent] = children
            else:
                valid[parent] = children[0]
        return valid, conflicting

def register():
    bpy.types.Scene.bs_prefix = bpy.props.StringProperty(
        name = "Prefix",
        description="Text that will be appended to the start of the new name.",
        default = "",
    )
    bpy.types.Scene.bs_suffix = bpy.props.StringProperty(
        name = "Suffix",
        description="Text that will be appended to the end of the new name.",
        default = "",
    )
    bpy.utils.register_class(BS_OT_RenameChildToMatchParent)

def unregister():
    del bpy.types.Scene.bs_prefix
    del bpy.types.Scene.bs_suffix
    bpy.utils.unregister_class(BS_OT_RenameChildToMatchParent)

if __name__ == "__main__":
    register()
