import bpy
from _bpy_types import Operator


class BS_OT_ShiftUVs(Operator):
    bl_idname = "bs.shift_uvs"
    bl_label = "Shift UVs"
    bl_description = "Shift UVs to the input coordinates"
    bl_options = {'REGISTER', 'UNDO'}

    x = bpy.props.IntProperty(
        name = "X",
        description = "X coordinate",
        min = 0,
    )

    y = bpy.props.IntProperty(
        name = "Y",
        description = "Y coordinate",
        min = 0,
    )

