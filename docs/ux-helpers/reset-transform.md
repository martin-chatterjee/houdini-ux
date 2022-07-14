---
layout: page
title: Reset Transform
permalink: /reset-transform/
parent: UX Helpers
nav_order: 5
---
<link rel="stylesheet" href="../assets/css/style.css">

# Reset Transform


---
### → Demo Hotkey:  `Alt + R`

---

**Zeroes out the local transforms** of all selected Objects.

**A frequent usage pattern is:**
- Multi-select two objects.
- `Parent()` → First object gets parented to second object
- `ResetTransform()` → Second child object "snaps" to the world transform of the parent object.
- `Unparent()` → Transformed child object gets unparented again.

→ This way the **world space transform of two objects can by synced** by selecting them, and then quickly executing:
- `Alt+P`
- `Alt+R`
- `Alt+Shift+P`