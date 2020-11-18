# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Martin Chatterjee. All rights reserved.
# -----------------------------------------------------------------------------
import hou
import toolutils

"""A collection of Houdini UX Helpers:

- **toggleFullScreen**:
  Toggles the Full Screen state of the Houdini Main Window.

- **toggleObjectDisplay**:
  Toggles the visibility of all selected Objects.

- **IsolateSelection**:
  Mimics the Maya/Softimage "Isolate Selection" workflow at the Objects level.

- **QuickDisplay**:
  Let's you store and load active/visible nodes in SOP's.
  This is intended to sort of mimic the UX behaviour of Nuke's viewer
  shortuts. (--> 1, 2, 3)

- **parent** & **unparent** selected objects

- **reset Transforms** for selected objects

- **walk hierarchy**  (up, down, left, right)


"""

# -----------------------------------------------------------------------------
def walkHierarchy(mode='up'):
    """
    """
    selected = [node for node in hou.selectedNodes()
                if node.type().category().name() == 'Object']
    result = []

    for item in selected:
        if mode == 'up':
            parent = item.input(0)
            if parent:
                result.append(parent)
        elif mode == 'down':
            outputs = item.outputs()
            if len(outputs):
                result.append(outputs[0])
        else:
            parent = item.input(0)
            if parent:
                siblings = parent.outputs()
                index = siblings.index(item)
                if mode == 'right':
                    index = (index + 1) % len(siblings)
                elif mode == 'left':
                    index = (index - 1) % len(siblings)
                result.append(siblings[index])

    if len(result):
        for item in selected:
            item.setSelected(False)
        for item in result:
            item.setSelected(True)

# -----------------------------------------------------------------------------
def resetTransform():
    """
    """
    selected = [node for node in hou.selectedNodes()
                if node.type().category().name() == 'Object']

    identity = hou.Matrix4()
    identity.setToIdentity()

    for item in selected:
        item.setParmTransform(identity)
        item.setPreTransform(identity)
        item.setParmPivotTransform(identity)


# -----------------------------------------------------------------------------
def parent():
    """
    """
    selected = [node for node in hou.selectedNodes()
                if node.type().category().name() == 'Object']
    if len(selected) < 2:
        return

    parent = selected[-1]
    children = selected[:-1]

    for child in children:
        child.parm('keeppos').set(True)
        child.setInput(0, parent)

    parent.setSelected(False)


# -----------------------------------------------------------------------------
def unparent():
    """
    """
    selected = [node for node in hou.selectedNodes()
                if node.type().category().name() == 'Object']

    for node in selected:
        node.parm('keeppos').set(True)
        node.setInput(0, None)



# -----------------------------------------------------------------------------
def toggleFullScreen():
    """Toggles the Full Screen state of the Houdini Main Window.
    """
    mw = hou.qt.mainWindow()
    if mw.isFullScreen():
        mw.showMaximized()
    else:
        mw.showFullScreen()


# -----------------------------------------------------------------------------
def toggleObjectDisplay():
    """Toggles the visibility flag of all selected Object-level Nodes.

    """
    objects = [item for item in hou.selectedNodes()
               if item.type().category().name() == 'Object']

    for node in objects:
        node.setDisplayFlag(not node.isDisplayFlagSet())


# -----------------------------------------------------------------------------
def isolateSelection():
    """Isolates the visibility of all currently selected Object-level nodes
    in all viewports and cameras.

    Acts as a toggle: If an isolation already exists it will remove it.

    """
    scene_view = toolutils.sceneViewer()
    viewport = scene_view.curViewport()
    settings = viewport.settings()

    current_mask = settings.visibleObjects()
    msg = ''
    if current_mask != '*':
        current_mask = '*'
        msg = ''
    else:
        isolate_me = []
        selected_object_nodes = [item for item in hou.selectedNodes()
                                 if item.type().category().name() == 'Object']
        for node in selected_object_nodes:
            isolate_me.append(node.path())
        current_mask = ' '.join(isolate_me)
        msg = '\n'.join(isolate_me)
        if msg != '':
            msg = '\n\nISOLATED\n--------------\n' + msg
        if current_mask == '':
            current_mask = '*'

    for viewport in scene_view.viewports():
        viewport.settings().setVisibleObjects(current_mask)
        viewport.draw()

    flash_msg = 'Isolate Selection'
    if msg == '':
        flash_msg = 'Display All'
    viewer = toolutils.sceneViewer()
    viewer.flashMessage('houdini_ux.png', flash_msg, 1.0)
    _ensureViewportMsg(msg)


# -----------------------------------------------------------------------------
def quickDisplay(slot):
    """Stores the currently selected first node as QuickDisplay identified
    by `slot`.

    QuickDisplay can only be used in a context with a data-flow paradigm such
    as SOP's.
    """
    viewer = toolutils.sceneViewer()
    path = viewer.pwd().path()

    # get first selected node in path
    selected_nodes = [item for item in hou.node(path).children()
                      if item.type().category().name() != 'Object'
                      and item.isSelected()]
    target = selected_nodes[0] if len(selected_nodes) else None
    if target:
        _storeQuickDisplayNode(path, slot, target)

    stored = _getStoredQuickDisplayNode(path, slot)
    if stored:
        stored.setDisplayFlag(True)
        stored.setRenderFlag(True)
        stored.setSelected(False)
        viewer.flashMessage('houdini_ux.png', 'QuickDisplay {}: {}'.format(slot, stored.name()), 1.0)


# -----------------------------------------------------------------------------
def clearQuickDisplay(full=False):
    """Clears the stored QuickDisplay nodes.
    """
    if full:
        hou.session.quick_display_storage = {}
    else:
        viewer = toolutils.sceneViewer()
        path = viewer.pwd().path()
        storage = _getQuickDisplayStorage(path)
        storage.clear()
        comment = 'QuickDisplay'
        for node in hou.node(path).children():
            if node.comment().startswith(comment):
                node.setComment('')

    viewer.flashMessage('houdini_ux.png', 'QuickDisplay: cleared', 1.5)


# -----------------------------------------------------------------------------
def _ensureViewportMsg(msg):
    """
    """
    cameras = hou.nodeType(hou.objNodeTypeCategory(), 'cam').instances()
    for cam in cameras:
        ptg = cam.parmTemplateGroup()
        folder = ptg.findFolder('Viewport Message')
        if not folder:
            folder = hou.FolderParmTemplate("folder", "Viewport Message")
            ptg.append(folder)
            cam.setParmTemplateGroup(ptg)
        param = None
        for item in folder.parmTemplates():
            if item.name() == 'vcomment':
                param = item
                break
        if not param:
            param = ptg.appendToFolder(folder, hou.StringParmTemplate("vcomment", "vcomment", 1))
            cam.setParmTemplateGroup(ptg)
        cam.parm('vcomment').set(msg)

# -----------------------------------------------------------------------------
def _getQuickDisplayStorage(path):
    """
    """
    if not hasattr(hou.session, 'quick_display_storage'):
        hou.session.quick_display_storage = {}
    storage = hou.session.quick_display_storage
    if not path in storage:
        storage[path] = {}
    return storage[path]

# -----------------------------------------------------------------------------
def _storeQuickDisplayNode(path, slot, node):
    """
    """
    storage = _getQuickDisplayStorage(path)
    storage[slot] = node.path()

    comment = 'QuickDisplay: {}'.format(slot)
    for child in hou.node(path).children():
        if child.comment() == comment:
            child.setComment('')
    node.setComment('QuickDisplay: {}'.format(slot))
    node.setGenericFlag(hou.nodeFlag.DisplayComment,True)


# -----------------------------------------------------------------------------
def _getStoredQuickDisplayNode(path, label):
    """
    """
    node = None
    storage = _getQuickDisplayStorage(path)
    stored_path = storage.get(label, None)
    if stored_path:
        node = hou.node(stored_path)
    return node
