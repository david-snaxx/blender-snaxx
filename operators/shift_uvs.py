import math
import bpy
from utils.getters import (get_selected_unique_mesh_objects)

class BS_OT_ShiftUVs(bpy.types.Operator):
    bl_idname = "bs.shift_uvs"
    bl_label = "Shift UVs"
    bl_description = "Shift UVs to the input coordinates"
    bl_options = {'REGISTER', 'UNDO'}

    # noinspection PyTypeHints
    uv_x: bpy.props.IntProperty(
        name = "x (u)",
        description = "x (u) coordinate to shift UVs to",
    )
    # noinspection PyTypeHints
    uv_y: bpy.props.IntProperty(
        name = "y (v)",
        description = "y (v) coordinate to shift UVs to",
    )

    def execute(self, context):
        meshes = get_selected_unique_mesh_objects(context)
        for mesh in meshes:
            move_active_uvs_to_tile_coords(mesh, self.uv_x, self.uv_y)
        self.report({"INFO"}, f"Finished shifting {len(meshes)} UVs")
        return {'FINISHED'}

def register():
    bpy.types.Scene.bs_uv_x = bpy.props.IntProperty(
        name = "x (u)",
        description = "x (u) coordinate to shift UVs to",
    )

    bpy.types.Scene.bs_uv_y = bpy.props.IntProperty(
        name = "y (v)",
        description = "y (v) coordinate to shift UVs to",
    )
    bpy.utils.register_class(BS_OT_ShiftUVs)

def unregister():
    del bpy.types.Scene.bs_uv_x
    del bpy.types.Scene.bs_uv_y
    bpy.utils.unregister_class(BS_OT_ShiftUVs)

if __name__ == "__main__":
    register()

def get_current_uv_tile_coords(obj):
    """Returns the (tile_u, tile_v) the mesh's UVs currently occupy,
    based on the floor of the lowest UV coordinates.
    u = horizontal, v = vertical"""
    uv_layer = obj.data.uv_layers.active.data
    us = []
    for loop_uv in uv_layer:
        us.append(loop_uv.uv.x)
    vs = []
    for loop_uv in uv_layer:
        vs.append(loop_uv.uv.y)
    return math.floor(min(us)), math.floor(min(vs))

def move_active_uvs_to_tile_coords(obj, tile_u, tile_v):
    ub_layer = obj.data.uv_layers.active.data
    current_u, current_v = get_current_uv_tile_coords(obj)
    offset_u = tile_u - current_u
    offset_v = tile_v - current_v
    for loop_uv in ub_layer:
        loop_uv.uv.x += offset_u
        loop_uv.uv.y += offset_v
