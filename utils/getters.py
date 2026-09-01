def get_selected_mesh_objects(context):
    meshes = []
    for obj in context.selected_objects:
        if obj.type == 'MESH':
            meshes.append(obj)
    return meshes

def get_mesh_armature(mesh_object):
    if mesh_object.parent and mesh_object.parent.type == 'ARMATURE':
        return mesh_object.parent
    for modifier in mesh_object.modifiers:
        if modifier.type == 'ARMATURE' and modifier.object:
            return modifier.object
    return None
