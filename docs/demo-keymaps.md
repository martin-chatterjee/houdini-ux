---
layout: page
title: Demo Keymaps
permalink: /demo-keymaps/
nav_order: 2
---
<link rel="stylesheet" href="../assets/css/style.css">

# A word about the Demo Keymaps

<br/>

**Houdini UX** ships with **two demo keymaps**:
- `houdini-ux-demo (minimal)`
- `houdini-ux-demo (with pickwalking)`

→ Just **save new unmodified keymaps** with **exactly** those names and the provided **Keymap Overrides** should be automatically picked up.\
_(→ see [Installation Instructions](../installation/#4-create-demo-hotkeys))_

<br/>

## An easy way to check out Houdini UX.

You can use these **demo keymaps** to quickly check out if you like any aspect of **Houdini UX**.

**Choosing hotkeys** always comes down to **personal preferences**, and often forces you to un-assign/re-assign other vanilla hotkeys to prevent conflicts.

### Therefore I'd like to suggest:
- Use these **demo keymaps** to **check things out**.
- If you like what you see, then **assign/manage your own hotkeys** to your liking in your own personal keymap.

<br/>

# Why are there two demo keymaps?
- The `houdini-ux-demo (minimal)` keymap provides hotkeys for **everything, except "Pickwalking/Hierarchy Walking"**.

- The `houdini-ux-demo (with pickwalking)` is a **bit more invasive**, as it **maps Pickwalking to the 4 cursor keys**.\
In Houdini the cursor keys control aspects of **timeline playback**, therefore these **had to be remapped** in this demo keymap, to "free" up the cursor keys.\
\
→ **Timeline Playback** has been mapped in here to the **vanilla Maya timeline hotkeys**:
    - Play Forward: `Alt+V`
    - Step Forward One: `Alt+.`
    - Step Backward One: `Alt+,`
    - Jump To Previous Keyframe: `,`
    - Jump To Next Keyframe: `.`

<br/>

## How do I assign my own hotkeys?
- Every command of **Houdini UX** also appears as a **shelf tool** in the `houdini-ux` shelf.
- You can **right-click** on such a **shelf tool**, and **assign a global hotkey** in the "Hotkeys" tab:

  ![edit-tool](../assets/images/edit-tool.png)
  ![hotkey-tab](../assets/images/hotkey-tab.png)
- For reference, **open** the **Houdini UX `.keymap.overrides` files** in a text editor to see what **hotkeys** get assigned in the **demo keymaps**. 
- Depending on your hotkey choices, the **Hotkey Manager** might prompt you to **de-assign/re-assign conflicting hotkeys**.
