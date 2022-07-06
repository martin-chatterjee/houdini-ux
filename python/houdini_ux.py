# -*- coding: utf-8 -*-
#
# Copyright (c) 2020-2022, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE)
# -----------------------------------------------------------------------------

"""A collection of Houdini UX Helpers:

- **Isolate Selection**:
  Mimics the Maya/Softimage "Isolate Selection" workflow at the Objects level.

- **Quick Display**:
  Let's you store and load active/visible nodes in SOP's.
  This is intended to sort of mimic the UX behaviour of Nuke's viewer
  shortuts. (--> 1, 2, 3)

- **Toggle Object Display**:
  Toggles the visibility of all selected objects.

- **Parent** & **Unparent** selected objects based on selection.

- **Reset Transforms** for selected objects.

- **Select Hierarchy** for selected objects.

- Setup **Pickwalking** for arbitrary objects.
  (→ Move between them using the up/down/left/right keys)

- **Toggle Full Screen**:
  Toggles the Full Screen state of the Houdini Main Window.

"""
import os

import hou
import toolutils


# -----------------------------------------------------------------------------
def isolate_selection():
    """Isolates the visibility of all currently selected Object-level nodes
    in all viewports and cameras.

    Acts as a toggle: If an isolation already exists it will remove it.

    """
    visibility_mask = "*"
    camera_viewport_message = ""

    is_active = _is_isolate_selection_active()

    if not is_active:
        selected_object_node_paths = [
            item.path()
            for item in hou.selectedNodes()
            if item.type().category().name() == "Object"
        ]
        if len(selected_object_node_paths):
            visibility_mask = " ".join(selected_object_node_paths)
            message_lines = [
                "",
                "",
                "ISOLATED",
                "--------------",
            ]
            message_lines.extend(selected_object_node_paths)
            camera_viewport_message = "\n".join(message_lines)

    _update_object_isolation_in_viewports(visibility_mask, camera_viewport_message)


# -----------------------------------------------------------------------------
def _is_isolate_selection_active():
    """Returns True if 'Isolate Selection' is currently active."""
    scene_viewer = toolutils.sceneViewer()
    viewport = scene_viewer.curViewport()
    settings = viewport.settings()
    current_mask = settings.visibleObjects()
    is_active = current_mask != "*"

    return is_active


# -----------------------------------------------------------------------------
def _update_object_isolation_in_viewports(visibility_mask, camera_viewport_message):
    """Updates the visibility mask for all viewports.

    Also displays HUD message in all cameras.

    """
    scene_viewer = toolutils.sceneViewer()
    for viewport in scene_viewer.viewports():
        viewport.settings().setVisibleObjects(visibility_mask)
        viewport.draw()
    flash_msg = "Display All" if visibility_mask == "*" else "Isolate Selection"
    scene_viewer.flashMessage("houdini_ux.png", flash_msg, 1.0)
    _show_message_in_cameras(camera_viewport_message)


# -----------------------------------------------------------------------------
def _show_message_in_cameras(msg):
    """Displays a HUD message in the top left corner of each camera viewport.

    Unfortunately this type of HUD message seems to only be possible in actual
    camera viewports at the moment.

    """
    cameras = hou.nodeType(hou.objNodeTypeCategory(), "cam").instances()
    for cam in cameras:
        ptg = cam.parmTemplateGroup()
        folder = ptg.findFolder("Viewport Message")
        if not folder:
            folder = hou.FolderParmTemplate("folder", "Viewport Message")
            ptg.append(folder)
            cam.setParmTemplateGroup(ptg)
        param = None
        for item in folder.parmTemplates():
            if item.name() == "vcomment":
                param = item
                break
        if not param:
            param = ptg.appendToFolder(
                folder, hou.StringParmTemplate("vcomment", "vcomment", 1)
            )
            cam.setParmTemplateGroup(ptg)
        cam.parm("vcomment").set(msg)


# -----------------------------------------------------------------------------
def quick_display(slot):
    """Stores the currently selected first node as QuickDisplay identified
    by `slot`.

    QuickDisplay can only be used in a context with a data-flow paradigm such
    as SOP's.
    """
    scene_viewer = toolutils.sceneViewer()
    path = scene_viewer.pwd().path()

    # get first selected node in path
    selected_nodes = [
        item
        for item in hou.node(path).children()
        if item.type().category().name() != "Object" and item.isSelected()
    ]
    target = selected_nodes[0] if len(selected_nodes) else None
    if target:
        _store_quick_display_node(path, slot, target)

    stored = _get_stored_quick_display_node(path, slot)
    if stored:
        stored.setDisplayFlag(True)
        stored.setRenderFlag(True)
        stored.setSelected(False)
        scene_viewer.flashMessage(
            "houdini_ux.png", "QuickDisplay {}: {}".format(slot, stored.name()), 1.0
        )


# -----------------------------------------------------------------------------
def clear_quick_display(full=False):
    """Clears the stored QuickDisplay nodes.

    If full is True, the full QuickDisplay storage gets cleared.
    Otherwise only the storage for the current view gets cleared.

    """
    if full:
        hou.session.quick_display_storage = {}
    else:
        scene_viewer = toolutils.sceneViewer()
        path = scene_viewer.pwd().path()
        storage = _get_quick_display_storage(path)
        storage.clear()
        comment = "QuickDisplay"
        for node in hou.node(path).children():
            if node.comment().startswith(comment):
                node.setComment("")

    scene_viewer.flashMessage("houdini_ux.png", "QuickDisplay: cleared", 1.5)


# -----------------------------------------------------------------------------
def _store_quick_display_node(path, slot, node):
    """Stores `node` in QuickDisplay `slot` for `path`.

    Also updates the node's comment to give a visual indication in the Network View.

    """
    storage = _get_quick_display_storage(path)
    storage[slot] = node.path()

    comment = "QuickDisplay: {}".format(slot)
    for child in hou.node(path).children():
        if child.comment() == comment:
            child.setComment("")
    node.setComment("QuickDisplay: {}".format(slot))
    node.setGenericFlag(hou.nodeFlag.DisplayComment, True)


# -----------------------------------------------------------------------------
def _get_quick_display_storage(path):
    """Retrieves and returns the QuickDisplay storage for `path`.

    If no storage exists for `path`, it will get initialized to {}.

    """
    if not hasattr(hou.session, "quick_display_storage"):
        hou.session.quick_display_storage = {}
    storage = hou.session.quick_display_storage
    if path not in storage:
        storage[path] = {}
    return storage[path]


# -----------------------------------------------------------------------------
def _get_stored_quick_display_node(path, slot):
    """Retrieves and returns the stored QuickDisplay labeled `slot` for `path`.

    Will return None if no node is stored.

    """
    node = None
    storage = _get_quick_display_storage(path)
    stored_path = storage.get(slot, None)
    if stored_path:
        node = hou.node(stored_path)
    return node


# -----------------------------------------------------------------------------
def toggle_object_display():
    """Toggles the visibility flag of all selected Object-level Nodes.

    - Each object's visibility will get toggled individually,
      enabling 'A/B' visibility flipping.
    - Selected objects can live anywhere in the scene hierarchy.

    """
    selected_objects = [
        item
        for item in hou.selectedNodes()
        if item.type().category().name() == "Object"
    ]

    for node in selected_objects:
        node.setDisplayFlag(not node.isDisplayFlagSet())


# -----------------------------------------------------------------------------
def parent():
    """Parents all other selected object nodes to the last selected object node.

    This effectively mimics Maya's parenting workflow in Houdini's 'obj' network.

    Objects the live on another network level than the designated parent object
    will **not** be parented.

    """
    selected_obj_nodes = [
        node
        for node in hou.selectedNodes()
        if node.type().category().name() == "Object"
    ]
    if len(selected_obj_nodes) < 2:
        return

    parent = selected_obj_nodes[-1]
    children = selected_obj_nodes[:-1]

    parent_level = os.path.dirname(parent.path())
    level_mismatch = False

    for child in children:
        # Ignore all children that are not on the same network level as parent.
        child_level = os.path.dirname(child.path())
        if child_level != parent_level:
            level_mismatch = True
            continue
        child.parm("keeppos").set(True)
        child.setInput(0, parent)

    if level_mismatch:
        flash_msg = (
            "Not all objects could be parented, "
            "as they live in different network depths."
        )
        scene_viewer = toolutils.sceneViewer()
        scene_viewer.flashMessage("houdini_ux.png", flash_msg, 3.0)
    parent.setSelected(False)


# -----------------------------------------------------------------------------
def unparent():
    """Unparents all selected object nodes."""
    selected_obj_nodes = [
        node
        for node in hou.selectedNodes()
        if node.type().category().name() == "Object"
    ]

    for node in selected_obj_nodes:
        node.parm("keeppos").set(True)
        node.setInput(0, None)


# -----------------------------------------------------------------------------
def reset_transform():
    """Resets the local transform of all selected object nodes."""
    selected_obj_nodes = [
        node
        for node in hou.selectedNodes()
        if node.type().category().name() == "Object"
    ]

    identity = hou.Matrix4()
    identity.setToIdentity()

    for item in selected_obj_nodes:
        item.setParmTransform(identity)
        item.setPreTransform(identity)
        item.setParmPivotTransform(identity)


# -----------------------------------------------------------------------------
def select_hierarchy():
    """Selects the full child hierarchy of any selected object nodes."""
    selected_obj_nodes = [
        node
        for node in hou.selectedNodes()
        if node.type().category().name() == "Object"
    ]

    def _select_recursively(node):
        node.setSelected(True)
        for child in node.outputs():
            _select_recursively(child)

    for node in selected_obj_nodes:
        _select_recursively(node)


# -----------------------------------------------------------------------------
def prepare_pickwalking():
    """ """
    selected = [
        node
        for node in hou.selectedNodes()
        if node.type().category().name() == "Object"
    ]

    for node in selected:
        _ensure_parm(node, "pw_up", "Up", folder_name="pickwalking")
        _ensure_parm(node, "pw_right", "Right", folder_name="pickwalking")
        _ensure_parm(node, "pw_down", "Down", folder_name="pickwalking")
        _ensure_parm(node, "pw_left", "Left", folder_name="pickwalking")


# -----------------------------------------------------------------------------
def pickwalk(mode="up", replace=True):
    """ """
    selected = [
        node
        for node in hou.selectedNodes()
        if node.type().category().name() == "Object"
    ]
    result = []

    for item in selected:
        pickwalk = item.parm("pw_{}".format(mode))
        if pickwalk:
            # target_path = pickwalk.eval()
            target = item.node(pickwalk.eval())
            if target:
                result.append(target)
                if replace:
                    item.setSelected(False)
        else:
            _walk_hierarchy(item, mode, result, replace)

    for item in result:
        item.setSelected(True, show_asset_if_selected=True)


# -----------------------------------------------------------------------------
def toggle_fullscreen():
    """Toggles the Full Screen state of the Houdini Main Window."""
    mw = hou.qt.mainWindow()
    if mw.isFullScreen():
        mw.showMaximized()
    else:
        mw.showFullScreen()


# -----------------------------------------------------------------------------
def _ensure_parm(node, parm_name, label_name, parm_start_value=None, folder_name=None):
    """ """
    parm = node.parm(parm_name)

    if not parm:
        folder = _ensure_parm_folder(node, folder_name=folder_name)

        ptg = node.parmTemplateGroup()
        parm_template = None

        parm_template = hou.StringParmTemplate(parm_name, label_name, 1)
        parm_template.setStringType(hou.stringParmType.NodeReference)
        if parm_start_value:
            parm_template.setDefaultValue((parm_start_value,))

        if parm_template:
            ptg.appendToFolder(folder, parm_template)
            node.setParmTemplateGroup(ptg)
            parm = node.parm(parm_name)
            if parm_start_value:
                parm.set(parm_start_value)

    return parm


# -----------------------------------------------------------------------------
def _ensure_parm_folder(node, folder_name):
    """ """
    ptg = node.parmTemplateGroup()
    folder = ptg.findFolder(folder_name)
    if not folder:
        folder = hou.FolderParmTemplate(
            name="fld_{}".format(folder_name.lower()), label=folder_name
        )
        ptg.append(folder)
        node.setParmTemplateGroup(ptg)
        ptg = node.parmTemplateGroup()
        folder = ptg.findFolder(folder_name)

    return folder


# -----------------------------------------------------------------------------
def _walk_hierarchy(item, mode, result, replace):
    """ """
    target = None

    if mode == "up":
        parent = item.input(0)
        if parent:
            target = parent
    elif mode == "down":
        outputs = item.outputs()
        if len(outputs):
            target = outputs[0]
    else:
        parent = item.input(0)
        if parent:
            siblings = parent.outputs()
            index = siblings.index(item)
            if mode == "right":
                index = (index + 1) % len(siblings)
            elif mode == "left":
                index = (index - 1) % len(siblings)
            target = siblings[index]

    if target:
        if replace:
            item.setSelected(False)
        result.append(target)
