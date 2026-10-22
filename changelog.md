# MultiFocus Changelog

## 1.1.0

### Added & Improved
- **Dynamic MultiFocus Mode**:
  - MultiFocus mode is disabled (OFF) by default to prevent key conflicts with other add-ons and applications.
  - Toggle mode anytime using **`NVDA+Windows+M`** (announces "MultiFocus mode on" or "MultiFocus mode off").
  - When **OFF**, all MultiFocus gestures are dynamically released and unbound, allowing standard NVDA and application shortcuts to execute without interference.
  - When **ON**, all MultiFocus gestures are dynamically bound and active.
  - The mode toggle shortcut (`NVDA+Windows+M`) always remains active.
  - Plugin termination cleanly unbinds only MultiFocus gestures.
- **Updated Gestures**:
  - `NVDA+Alt+F` to toggle between recent cursors (removed `NVDA+Alt+C`).
  - `NVDA+Ctrl+1` through `9` to directly jump to saved cursors.
  - `NVDA+Shift+1` through `9` to directly assign saved cursors.

## 1.0.0

Initial release of MultiFocus - Multiple Cursors & Focus Manager for NVDA.

### Features
- Create and save multiple cursors at different positions with `NVDA+Shift+C`.
- Quick toggle between recent cursor positions.
- Cycle forward and backward through saved cursors with `NVDA+Alt+Right Arrow` and `NVDA+Alt+Left Arrow`.
- Interactive Cursor Manager dialog with `NVDA+Alt+L` (double-press) or audio summary (single-press).
- Quick help audio guide with `NVDA+Alt+H`.
- Audio peek around alternate cursors without moving active focus (`NVDA+Alt+Down Arrow`, `NVDA+Alt+Up Arrow`, `NVDA+Alt+Shift+C`).
- Delete active cursor (`NVDA+Alt+Delete`) or clear all cursors (`NVDA+Alt+Shift+Delete`).
- Direct numbered slot assignment (`NVDA+Shift+1..9`) and jumping.
- Automatic application window switching when restoring cursor positions.
- All gestures customizable via NVDA's Input Gestures dialog.
