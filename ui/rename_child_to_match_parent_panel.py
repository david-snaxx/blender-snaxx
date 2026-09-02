import bpy
from ..operators import (rename_child_to_match_parent)

def draw_rename_child_to_match_parent(context, layout, scene):
    header, panel = layout.panel("bs_rename_child_to_match_parent", default_closed=False)
    header.label(text="Rename child to match parent", icon="TEXT")
    if panel:
        panel.prop(scene, "bs_prefix")
        panel.prop(scene, "bs_suffix")
        op = panel.operator("bs.rename_child_to_match_parent", text="Rename child to match parent")
        op.suffix = scene.bs_suffix
        op.prefix = scene.bs_prefix
        # preview
        preview_box = panel.box()
        preview_header, preview_panel = preview_box.panel("bs_rename_child_to_match_parent_preview", default_closed=True)
        preview_header.label(text="Preview")
        if preview_panel:
            parent_child_dict = (rename_child_to_match_parent
                                 .BS_OT_RenameChildToMatchParent
                                 .get_parent_child_grouping(context.selected_objects))
            valid, conflicting = (rename_child_to_match_parent
                                  .BS_OT_RenameChildToMatchParent
                                  .split_parent_child_groups_to_valid_and_conflicting(parent_child_dict))
            if valid:
                sub = preview_panel.box()
                sub.label(text=f"Found {len(valid)} objects:", icon="CHECKMARK")
                for parent, child in valid.items():
                    row = sub.row()
                    row.label(text=f"{child.name} ...->... {scene.bs_prefix}{parent.name}{scene.bs_suffix}")

            if conflicting:
                sub = preview_panel.box()
                sub.label(text=f"Conflicting selections (these objects will not be renamed):", icon="ERROR")
                for parent, children in conflicting.items():
                    row = sub.row()
                    entry_text = ""
                    for child in children:
                        entry_text += f"{child.name}, "
                    entry_text = entry_text[:-2]
                    parent_label = ""
                    if parent is None:
                        parent_label = "(no parent)"
                    else:
                        parent_label = f"{parent.name}"
                    entry_text += f" ...share parent... {parent_label}"
                    row.label(text=entry_text)
