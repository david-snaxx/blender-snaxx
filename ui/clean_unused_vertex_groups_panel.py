import bpy
from ..utils.getters import (get_selected_mesh_objects,
                           get_mesh_armature)

def draw_clean_unused_vertex_groups(context, layout, scene):
    header, panel = layout.panel("bs_clean_unused_vertex_groups", default_closed = False)
    header.label(text = "Clean unused vertex groups", icon = "GROUP_VERTEX")
    if panel:
        panel.use_property_split = True
        panel.use_property_decorate = False
        col = panel.column()
        col.prop(scene, "bs_remove_unweighted")
        col.prop(scene, "bs_remove_unassigned")
        panel.separator()
        row = panel.row()
        row.alignment = 'CENTER'
        row.scale_y = 1.4
        op = row.operator("bs.clean_unused_vertex_groups", text="Clean unused vertex groups", icon="GHOST_ENABLED")
        op.remove_unweighted = scene.bs_remove_unweighted
        op.remove_unassigned = scene.bs_remove_unassigned
        # preview
        preview_header, preview_panel = panel.panel("bs_clean_unused_vertex_groups_preview", default_closed = True)
        preview_header.label(text="Preview")
        if preview_panel:
            selected_mesh_objects = get_selected_mesh_objects(context)
            has_armature = set()
            no_armature = set()
            for obj in selected_mesh_objects:
                armature = get_mesh_armature(obj)
                if armature is not None:
                    has_armature.add(obj)
                else:
                    no_armature.add(obj)
            if not has_armature and not no_armature:
                preview_panel.label(text="No valid objects selected", icon="INFO")
            if has_armature:
                sub = preview_panel.box()
                sub.label(text=f"Found {len(has_armature)} mesh objects with armature:", icon="CHECKMARK")
                for obj in has_armature:
                    row = sub.row()
                    row.label(text=obj.name)
            if no_armature:
                sub = preview_panel.box()
                sub.label(text=f"Found {len(no_armature)} mesh objects with no armature:", icon="ERROR")
                sub.label(text="unassigned clean operation will not run on these objects")
                for obj in no_armature:
                    row = sub.row()
                    row.label(text=obj.name)
