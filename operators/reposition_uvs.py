import bpy, math
from ..utils.getters import get_selected_mesh_objects

class BS_OT_RepositionUVs(bpy.types.Operator):
    bl_idname = "bs.reposition_uvs"
    bl_label = "Reposition UVs"
    bl_description = "Reposition UVs to the exact UV space tile coordinates"
    bl_options = {'REGISTER', 'UNDO'}

    # noinspection PyTypeHints
    reposition_x: bpy.props.IntProperty(
        name = "x (u)",
        description = "x (u) coordinate to shift UVs to",
    )
    # noinspection PyTypeHints
    reposition_y: bpy.props.IntProperty(
        name = "y (v)",
        description = "y (v) coordinate to shift UVs to",
    )
    # noinspection PyTypeHints
    reposition_target: bpy.props.EnumProperty(
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
            if self.reposition_target == "ACTIVE":
                reposition_active_uvs_to_tile_coords(mesh, self.reposition_x, self.reposition_y)
            elif self.reposition_target == "ALL":
                reposition_all_uvs_to_tile_coords(mesh, self.reposition_x, self.reposition_y)
            else:
                self.report({'ERROR'}, "Unknown error, no move target found")
                return {'CANCELLED'}
        self.report({"INFO"}, f"Finished shifting {len(meshes)} UVs")
        return {'FINISHED'}

def register():
    bpy.types.Scene.bs_reposition_x = bpy.props.IntProperty(
        name = "x (u)",
        description = "x (u) coordinate to shift UVs to",
    )
    bpy.types.Scene.bs_reposition_y = bpy.props.IntProperty(
        name = "y (v)",
        description = "y (v) coordinate to shift UVs to",
    )
    bpy.types.Scene.bs_reposition_target = bpy.props.EnumProperty(
        name="UV Maps to Move",
        description="Which UV map(s) to shift",
        items=[
            ('ACTIVE', "Active UV Map Only", "Move only the currently active UV map of the selected meshes"),
            ('ALL', "All UV Maps", "Move all UV maps of the selected meshes"),
        ],
        default='ALL',
    )
    bpy.utils.register_class(BS_OT_RepositionUVs)

def unregister():
    del bpy.types.Scene.bs_reposition_x
    del bpy.types.Scene.bs_reposition_y
    del bpy.types.Scene.bs_reposition_target
    bpy.utils.unregister_class(BS_OT_RepositionUVs)

if __name__ == "__main__":
    register()

def reposition_active_uvs_to_tile_coords(obj, tile_u, tile_v):
    ub_layer = obj.data.uv_layers.active.data
    current_u, current_v = get_current_uv_tile_coords(obj)
    offset_u = tile_u - current_u
    offset_v = tile_v - current_v
    for loop_uv in ub_layer:
        loop_uv.uv.x += offset_u
        loop_uv.uv.y += offset_v

def reposition_all_uvs_to_tile_coords(obj, tile_u, tile_v):
    for uv_layer in obj.data.uv_layers:
        current_u, current_v = get_current_uv_tile_coords(obj)
        offset_u = tile_u - current_u
        offset_v = tile_v - current_v
        for loop_uv in uv_layer:
            loop_uv.uv.x += offset_u
            loop_uv.uv.y += offset_v

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
