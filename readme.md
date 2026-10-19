# MultiFocus - Multiple Cursors & Virtual Focuses for NVDA

* **Author**: Pawan Kumar
* **Version**: 1.0

**MultiFocus** brings intuitive multiple cursors and virtual focus navigation to the NVDA screen reader across applications, web pages, and documents.

MultiFocus allows you to save your place anywhere in Windows, jump back and forth, cycle through multiple locations, or browse your saved cursors in a visual and screen-reader-friendly dialog.

---

## Quick Start (Only 3 Keys to Remember!)

1. **Save Your Spot**: Press **`NVDA + Shift + C`**
   * Drops a cursor at your current position. NVDA confirms with a chime and preview.
2. **Jump / Toggle Back & Forth**: Press **`NVDA + Alt + C`** (or `NVDA + Alt + F`)
   * Instantly flips between your two most recent positions.
3. **Browse or Manage Cursors**: Press **`NVDA + Alt + L`**
   * **Press once**: Speaks a quick summary of your active cursors.
   * **Press twice quickly**: Opens the **MultiFocus Cursor Manager dialog** where you can arrow through your cursors, press **Enter** to jump, or **Delete** to remove.

> [!TIP]
> Forgot a shortcut? Press **`NVDA + Alt + H`** anytime for an instant audio reminder of the main keys!

---

## Keystroke Reference

### Everyday Essentials
| Keystroke | Action | Description |
| :--- | :--- | :--- |
| **`NVDA + Shift + C`** | **Save Cursor** | Saves a new cursor at your current position. |
| **`NVDA + Alt + C`** *(or `Alt+F`)* | **Toggle Recent** | Switches between your current and previous cursor. |
| **`NVDA + Alt + Right Arrow`** | **Next Cursor** | Cycles forward to the next saved cursor. |
| **`NVDA + Alt + Left Arrow`** | **Previous Cursor** | Cycles backward to the previous saved cursor. |
| **`NVDA + Alt + L`** | **List / Manager** | Press once for audio list; press twice to open the **Cursor Manager Dialog**. |
| **`NVDA + Alt + H`** | **Quick Help** | Speaks a brief audio guide of essential shortcuts. |

### Audio Peek (Inspect Without Moving Focus)
| Keystroke | Action | Description |
| :--- | :--- | :--- |
| **`NVDA + Alt + Down Arrow`** | **Peek Next Line** | Reads next line at alternate cursor without moving active focus. |
| **`NVDA + Alt + Up Arrow`** | **Peek Previous Line** | Reads previous line at alternate cursor without moving active focus. |
| **`NVDA + Alt + Shift + C`** | **Peek Current Line** | Reads current line at alternate cursor without moving active focus. |

### Cursor Management
| Keystroke | Action | Description |
| :--- | :--- | :--- |
| **`NVDA + Alt + Delete`** | **Delete Cursor** | Deletes the active cursor. |
| **`NVDA + Alt + Shift + Delete`** | **Clear All** | Removes all saved cursors. |

### Direct Slots (For Advanced Users)
* **`NVDA + Shift + 1` through `9`**: Directly assigns current position to Cursor 1 through 9.
* **`NVDA + Alt + 1` through `9`**: Directly jumps to Cursor 1 through 9.

> [!NOTE]
> All keystrokes can be rebound via **NVDA Menu > Preferences > Input Gestures > MultiFocus (Multiple Cursors)**.

---

## Example Use Cases

* **Reference Notes & Writing**: Keep Cursor 1 inside your document or editor, and Cursor 2 on reference material or questions. Toggle seamlessly with `NVDA + Alt + C`.
* **Cross-Application Work**: Mark a cell in Excel as Cursor 1 and an email in Outlook as Cursor 2. MultiFocus automatically brings the respective window to the front.
* **Web Form Filling**: Mark guidelines or instructions as Cursor 2, and type your answers at Cursor 1. Peek at lines with `NVDA + Alt + Down Arrow` without losing your form field focus!
