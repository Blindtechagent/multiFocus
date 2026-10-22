# MultiFocus - Multiple Cursors & Virtual Focuses for NVDA

* **Author**: Pawan Kumar
* **Version**: 1.1.0

**MultiFocus** brings intuitive multiple cursors and virtual focus navigation to the NVDA screen reader across applications, web pages, and documents.

MultiFocus allows you to bookmark your place anywhere in Windows, jump back and forth, cycle through multiple locations, or browse your saved cursors in an accessible dialog.

---

## Dynamic MultiFocus Mode

To avoid unwanted shortcut conflicts with NVDA commands or third-party applications, MultiFocus features a dynamic mode toggle:

* **OFF by default**: When NVDA starts, MultiFocus is disabled.
* **Toggle Shortcut**: Press **`NVDA + Windows + M`** to toggle MultiFocus ON or OFF at any time (NVDA announces "MultiFocus mode on" or "MultiFocus mode off").
* **Released while OFF**: When MultiFocus is OFF, all MultiFocus gestures are dynamically released and unbound so that standard NVDA and Windows shortcuts work normally without interception.
* **Active while ON**: When MultiFocus is ON, all MultiFocus shortcuts are dynamically bound and responsive.
* **Always Available**: The mode toggle shortcut (**`NVDA + Windows + M`**) always remains active.
* **Safe Cleanup**: Plugin termination or reload releases only MultiFocus gesture bindings.

---

## Quick Start

1. **Enable MultiFocus**: Press **`NVDA + Windows + M`** (announces "MultiFocus mode on").
2. **Save Your Position**: Press **`NVDA + Shift + C`** to drop a cursor at your active focus or caret position.
3. **Toggle Back & Forth**: Press **`NVDA + Alt + F`** to flip instantly between your two most recent positions.
4. **Browse Cursors**: Press **`NVDA + Alt + L`** once for an audio summary, or press twice quickly to open the **Cursor Manager dialog**.

> [!TIP]
> Forgot a shortcut? Press **`NVDA + Alt + H`** for an immediate audio reminder of essential shortcuts!

---

## Complete Keystroke Reference Table

| Keystroke | Action | Description |
| :--- | :--- | :--- |
| **`NVDA + Windows + M`** | **Toggle MultiFocus** | Toggles MultiFocus mode ON or OFF (OFF by default). Always available. |
| **`NVDA + Shift + C`** | **Save Cursor** | Saves a new cursor at your current position. |
| **`NVDA + Alt + F`** | **Toggle Recent** | Switches between your current and previous cursor. |
| **`NVDA + Alt + Right Arrow`** | **Next Cursor** | Cycles forward to the next saved cursor. |
| **`NVDA + Alt + Left Arrow`** | **Previous Cursor** | Cycles backward to the previous saved cursor. |
| **`NVDA + Alt + L`** | **List / Manager** | Press once for audio list; press twice to open the **Cursor Manager Dialog**. |
| **`NVDA + Alt + H`** | **Quick Help** | Speaks a brief audio guide of essential shortcuts. |
| **`NVDA + Alt + Down Arrow`** | **Peek Next** | Reads next line at alternate cursor without moving active focus. |
| **`NVDA + Alt + Up Arrow`** | **Peek Previous** | Reads previous line at alternate cursor without moving active focus. |
| **`NVDA + Alt + Shift + C`** | **Peek Current** | Reads current line at alternate cursor without moving active focus. |
| **`NVDA + Alt + Delete`** | **Delete Cursor** | Deletes the active cursor. |
| **`NVDA + Alt + Shift + Delete`** | **Clear All** | Removes all saved cursors. |
| **`NVDA + Shift + 1` .. `9`** | **Set Cursor 1..9** | Directly assigns current position to Cursor 1 through 9. |
| **`NVDA + Ctrl + 1` .. `9`** | **Jump Cursor 1..9** | Directly jumps to Cursor 1 through 9 and restores focus/caret. |

> [!NOTE]
> All keystrokes can be rebound via **NVDA Menu > Preferences > Input Gestures > MultiFocus (Multiple Cursors)**.

---

## Example Use Cases

* **Reference Notes & Writing**: Keep Cursor 1 inside your document or editor, and Cursor 2 on reference material. Toggle seamlessly with `NVDA + Alt + F`.
* **Cross-Application Work**: Mark a cell in Excel as Cursor 1 and an email in Outlook as Cursor 2. MultiFocus automatically brings the respective window to the front.
* **Web Form Filling**: Mark guidelines or instructions as Cursor 2, and type answers at Cursor 1. Peek at lines with `NVDA + Alt + Down Arrow` without losing your input focus!

---

## Contact & Feedback

* **Author**: Pawan Kumar
* **Telegram**: [https://t.me/pawan_ks](https://t.me/pawan_ks)
* **Email**: [pawanpianoartist@gmail.com](mailto:pawanpianoartist@gmail.com)
* **Repository**: [https://github.com/Blindtechagent/multiFocus](https://github.com/Blindtechagent/multiFocus)
