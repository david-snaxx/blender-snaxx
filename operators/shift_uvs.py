import math
import bpy

from ..utils.getters import get_selected_mesh_objects


class BS_OT_ShiftUVs(bpy.types.Operator):
    bl_idname = "bs.shift_uvs"
    bl_label = "Shift UVs"
    bl_description = ("Moves the UVs of the currently selected meshes by the input x/y amount. Positive x values move "
                      "up, negative x move down, and the same behavior applies on the y axis.")
    bl_options = {'REGISTER', 'UNDO'}

    # noinspection PyTypeHints
    move_x: bpy.props.IntProperty(
        name="x (u)",
        description="Shift selected mesh UVs vertically (x) by this amount"
    )
    # noinspection PyTypeHints
    move_y: bpy.props.IntProperty(
        name="y (u)",
        description="Shift selected mesh UVs horizontally (y) by this amount"
    )
    # noinspection PyTypeHints
    move_target: bpy.props.EnumProperty(
        name="UV Maps to Move",
        description="Which UV map(s) to shift",
        items=[
            ('ACTIVE', "Active UV Map Only", "Move only the currently active UV map of the selected meshes"),
            ('ALL', "All UV Maps", "Move all UV maps of the selected meshes"),
        ],
        default='ALL',
    )

    def execute(self, context):
        meshes = get_selected_mesh_objects(context)
        for mesh in meshes:
            if self.move_target == 'ACTIVE':
                adjust_active_uv_map_by_amount(mesh, self.move_x, self.move_y)
            elif self.move_target == 'ALL':
                adjust_all_uv_maps_by_amount(mesh, self.move_x, self.move_y)
            else:
                self.report({'ERROR'}, "Unknown error, no move target found")
                return {'CANCELLED'}
        self.report({"INFO"}, f"Finished shifting {len(meshes)} UVs")
        return {'FINISHED'}


def register():
    bpy.types.Scene.bs_move_x = bpy.props.IntProperty(
        name="x (u)",
        description="Shift selected mesh UVs vertically (x) by this amount"
    )
    bpy.types.Scene.bs_move_y = bpy.props.IntProperty(
        name="y (v)",
        description="Shift selected mesh UVs horizontally (y) by this amount"
    )
    bpy.types.Scene.bs_move_target = bpy.props.EnumProperty(
        name="UV Maps to Move",
        description="Which UV map(s) to shift",
        items=[
            ('ACTIVE', "Active UV Map Only", "Move only the currently active UV map of the selected meshes"),
            ('ALL', "All UV Maps", "Move all UV maps of the selected meshes"),
        ],
        default='ALL',
    )
    bpy.utils.register_class(BS_OT_ShiftUVs)

def unregister():
    del bpy.types.Scene.bs_move_x
    del bpy.types.Scene.bs_move_y
    del bpy.types.Scene.bs_move_target
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
