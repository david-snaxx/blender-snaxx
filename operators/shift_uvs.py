import math
import bpy

from ..utils.getters import get_selected_mesh_objects

class BS_OT_ShiftUVs(bpy.types.Operator):
    bl_idname = "bs.shift_uvs"
    bl_label = "Shift UVs"
    bl_description = "Shift UVs to the input coordinates"
    bl_options = {'REGISTER', 'UNDO'}

    # # noinspection PyTypeHints
    # uv_x: bpy.props.IntProperty(
    #     name = "x (u)",
    #     description = "x (u) coordinate to shift UVs to",
    # )
    # # noinspection PyTypeHints
    # uv_y: bpy.props.IntProperty(
    #     name = "y (v)",
    #     description = "y (v) coordinate to shift UVs to",
    # )

    # noinspection PyTypeHints
    move_x: bpy.props.IntProperty(
        name = "x (u)",
        description = "Shift selected mesh UVs vertically (x) by this amount"
    )
    # noinspection PyTypeHints
    move_y: bpy.props.IntProperty(
        name = "y (u)",
        description = "Shift selected mesh UVs horizontally (y) by this amount"
    )
    # noinspection PyTypeHints
    move_active_uv_map: bpy.props.BoolProperty(
        name = "Active UV Map Only",
        description = "Move only the currently active UV map of the selected meshes",
        default = False,
    )
    # noinspection PyTypeHints
    move_all_uv_maps: bpy.props.BoolProperty(
        name = "Move all UV Maps",
        description = "Move all UV maps of the selected meshes",
        default = False,
    )

    def execute(self, context):
        meshes = get_selected_mesh_objects(context)
        for mesh in meshes:
            if self.move_active_uv_map and self.move_all_uv_maps:
                self.report({"ERROR"}, "Must only select one option among active/all UV maps")
                return {"CANCELLED"}
            if self.move_active_uv_map:
                adjust_active_uv_map_by_amount(mesh, self.move_x, self.move_y)
            elif self.move_all_uv_maps:
                adjust_all_uv_maps_by_amount(mesh, self.move_x, self.move_y)
            else:
                self.report({"ERROR"}, "Must select active/all UV maps to adjust")
                return {"CANCELLED"}
        self.report({"INFO"}, f"Finished shifting {len(meshes)} UVs")
        return {'FINISHED'}

def register():
    # bpy.types.Scene.bs_uv_x = bpy.props.IntProperty(
    #     name = "x (u)",
    #     description = "x (u) coordinate to shift UVs to",
    # )
    #
    # bpy.types.Scene.bs_uv_y = bpy.props.IntProperty(
    #     name = "y (v)",
    #     description = "y (v) coordinate to shift UVs to",
    # )

    bpy.types.Scene.bs_move_x = bpy.props.IntProperty(
        name = "x (u)",
        description = "Shift selected mesh UVs vertically (x) by this amount"
    )
    bpy.types.Scene.bs_move_y = bpy.props.IntProperty(
        name = "y (u)",
        description = "Shift selected mesh UVs horizontally (y) by this amount"
    )
    bpy.types.Scene.bs_move_active_uv_map = bpy.props.BoolProperty(
        name = "Active UV Map Only",
        description = "Move only the currently active UV map of the selected meshes",
        default = False,
    )
    bpy.types.Scene.bs_move_all_uv_maps = bpy.props.BoolProperty(
        name = "Move all UV Maps",
        description = "Move all UV maps of the selected meshes",
        default = False,
    )
    bpy.utils.register_class(BS_OT_ShiftUVs)

def unregister():
    # del bpy.types.Scene.bs_uv_x
    # del bpy.types.Scene.bs_uv_y
    del bpy.types.Scene.bs_move_x
    del bpy.types.Scene.bs_move_y
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

# def move_active_uvs_to_tile_coords(obj, tile_u, tile_v):
#     ub_layer = obj.data.uv_layers.active.data
#     current_u, current_v = get_current_uv_tile_coords(obj)
#     offset_u = tile_u - current_u
#     offset_v = tile_v - current_v
#     for loop_uv in ub_layer:
#         loop_uv.uv.x += offset_u
#         loop_uv.uv.y += offset_v

def adjust_active_uv_map_by_amount(obj, x, y):
    active_uv_layer = obj.data.uv_layers.active.data
    for loop_uv in active_uv_layer:
        loop_uv.uv.x += x
        loop_uv.uv.y += y

def adjust_all_uv_maps_by_amount(obj, x, y):
    for uv_layer in obj.data.uv_layers:
        for loop_uv in uv_layer.data:
            loop_uv.uv.x += x
            loop_uv.uv.y += y