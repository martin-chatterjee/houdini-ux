
# ![headline](logo.png)

<br/>
<br/>

### A collection of **Houdini UX Helpers**:

- **toggleFullScreen**:
  Toggles the Full Screen state of the Houdini Main Window.

- **toggleObjectDisplay**:
  Toggles the visibility of all selected Objects.

- **IsolateSelection**:
  Mimics the Maya/Softimage "Isolate Selection" workflow at the Objects level.

- **QuickDisplay**:
  Let's you store and load active/visible nodes in SOP's.<br/>
  This is intended to sort of mimic the UX behaviour of **Nuke's viewer**
  shortcuts. (--> 1, 2, 3)

- **parent** & **unparent** selected objects

- **reset Transform** of selected objects

- **pickwalking**  (up, down, left, right)


<br/>

### Installation:

- copy ``packages/houdini_ux.json`` into your ``$HFS/packages`` Folder.
- update the **path** inside the ``houdini_ux.json`` so that it points to this repo.
- start Houdini
- verify that the package got picked up:
    - in a **Python Shell**:  ``import houdini_ux; print(houdini_ux)``
- display the **houdiniUX** shelf
- add **Hotkeys** to all shelf items.


<br/>

### My Hotkey suggestions:


**Move these Vanilla Hotkeys for Animation Control:**

- Play Forward                UpArrow     -->     Alt+V
- Step Forward One            RightArrow  -->     Alt+.
- Step Backward One           LeftArrow   -->     Alt+,
- Jump To Previous Keyframe               -->     ,
- Jump To Next Keyframe                   -->     .


**Then set houdini-ux hotkeys (these are my suggestions):**

- **toggleFullScreen**      : F11

- **toggleDisplayFlags**    : Alt+H
- **isolateSelection**      : Alt+I

- **quickDisplay Clear**    : Ctrl+`
- **quickDisplay A**        : Ctrl+F1
- **quickDisplay B**        : Ctrl+F2
- **quickDisplay C**        : Ctrl+F3

- **parent**                : Alt+P
- **unparent**              : Shift+P
- **reset Transform**       : Alt+R

- **Pick Walk up**               : Up
- **Pick Walk down**             : Down
- **Pick Walk left**             : Left
- **Pick Walk right**            : Right

- **Pick Walk Add up**               : Shift+Up
- **Pick Walk Add down**             : Shift+Down
- **Pick Walk Add left**             : Shift+Left
- **Pick Walk Add right**            : Shift+Right
