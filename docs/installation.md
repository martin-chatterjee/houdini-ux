---
layout: page
title: Installation
permalink: /installation/
nav_order: 1
---
<link rel="stylesheet" href="../assets/css/style.css">

# Installation Instructions

**Houdini UX** is distributed and loaded as a [**Houdini package**](https://www.sidefx.com/docs/houdini/ref/plugins.html).

<br/>

## 1. Download Release.
- **Visit** [Houdini UX on GitHub](https://github.com/martin-chatterjee/houdini-ux) and **download** the `.zip` or `.tar.gz` file of the **latest release**.

   ![github-releases](../assets/images/github-releases.png)

- **Unzip** it to anywhere you want and **rename** the top folder back to `houdini-ux`.

_(→ Or just **clone the repo** of course, if you are git-savvy and prefer that...)_

<br/>

## 2. Copy and adjust package file.

- **Copy** ``package_template/houdini_ux.json`` into your **home folder**: `$HOUDINI_USER_PREF_DIR/packages`.\
   _(→ Or into [any other folder](https://www.sidefx.com/docs/houdini/ref/plugins.html#using_packages) where **Houdini package files** will get picked up.)_
   
- **Update** the **`HUX_ROOT`** env variable defined inside this ``houdini_ux.json`` file so that it **points to your `houdini-ux` location**:

   ![headline](../assets/images/package-json.png)

<br/>

## 3. Verify that package gets loaded.
- **Start** Houdini.
- **Verify** that the package got picked up:
   - in a **Python Shell** inside Houdini:

     ![python-shell](../assets/images/python-shell.png)
     ```python
     >>> import houdini_ux
     >>> print(houdini_ux)
     <module 'houdini_ux' from '/path/to/houdini-ux/python/houdini_ux.py'>
     ```
- **Display** the **houdini-ux** shelf:

     ![houdini-ux-shelf](../assets/images/houdini-ux-shelf.png)

<br/>

## 4. Create Demo Hotkeys
- Open the **Hotkey Manager** in Houdini.
- Click on the **Gears** icon and click **"Save As..."**:\
    ![hotkey-manager](../assets/images/hotkey-manager.png)
- **Save** a new keymap with **exactly** this name: 
   ```
houdini-ux-demo (minimal)
```
    ![keymap-minimal](../assets/images/keymap-minimal.png)
- Now **switch back** to the **Houdini** keymap and then **save** another keymap with **exactly** this name:
   ```
houdini-ux-demo (with pickwalking)
```

---
> **NOTE:** The `houdini-ux` package contains **Keymap Overrides** that will **automatically get picked** up by correctly named keymaps.

---

- Now **activate one** of the **demo keymaps**.\
  _(If in doubt, start with `houdini-ux-demo (minimal)`.)_

<br/>

## 5. Verify that the Keymap Overrides got picked up.
- **Select** anything in the **Objects** context and hit `Alt+I` (→ "Isolate Selection").

### → This should happen:

  ![isolate-selection](../assets/images/isolate-selection.gif)

<br/>

## That should be it! :) 

You're now ready to check out **Houdini UX**.