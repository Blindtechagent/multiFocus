# -*- coding: UTF-8 -*-
"""
Focus & Multiple Cursors Manager for NVDA.
Allows creating, cycling, toggling, peeking, and managing multiple independent
cursors / focus points across any application, web page, or document.
"""

from dataclasses import dataclass
from typing import Optional, Any, Dict, List
import wx
import api
import textInfos
import controlTypes
import speech
import ui
from .soundEffects import (
    play_cursor_set_sound,
    play_cursor_switch_sound,
    play_cycle_sound,
    play_cursor_delete_sound,
    play_peek_sound,
    play_error_sound
)

try:
    _ = _
except NameError:
    def _(msg):
        return msg


@dataclass
class CursorPoint:
    """Represents an independent NVDA cursor / focus position."""
    index: int
    name: str
    app_name: str
    obj: Any
    root_obj: Any
    is_tree_interceptor: bool
    tree_interceptor: Any
    was_pass_through: bool
    bookmark: Any
    snippet: str
    _peek_info: Any = None

    def get_peek_info(self):
        """Creates or returns an independent TextInfo for peeking without moving active cursor."""
        try:
            if self._peek_info is not None:
                return self._peek_info

            if self.is_tree_interceptor and self.tree_interceptor and getattr(self.tree_interceptor, 'isAlive', False):
                if self.bookmark:
                    info = self.tree_interceptor.makeTextInfo(self.bookmark)
                else:
                    info = getattr(self.tree_interceptor, 'selection', None)
                    if not info:
                        info = self.tree_interceptor.makeTextInfo(textInfos.POSITION_CARET)
                self._peek_info = info
                return self._peek_info

            target_obj = self.obj if (self.obj and getattr(self.obj, 'isAlive', True)) else self.root_obj
            if target_obj and getattr(target_obj, 'isAlive', True):
                if self.bookmark:
                    info = target_obj.makeTextInfo(self.bookmark)
                else:
                    info = target_obj.makeTextInfo(textInfos.POSITION_CARET)
                self._peek_info = info
                return self._peek_info
        except Exception:
            return None
        return None

    def reset_peek(self):
        """Resets peek cursor back to original location."""
        self._peek_info = None


class MultiCursorManager:
    """Manages multiple independent cursors and virtual focus positions."""

    def __init__(self, max_slots: int = 9):
        self.max_slots = max_slots
        self.cursors: Dict[int, Optional[CursorPoint]] = {i: None for i in range(1, max_slots + 1)}
        self.active_cursor_index: int = 1
        self.previous_cursor_index: int = 1

    def capture_point(self, index: int, custom_name: str = "") -> Optional[CursorPoint]:
        """Captures the current NVDA focus, virtual cursor, and caret state."""
        focus_obj = api.getFocusObject()
        if not focus_obj:
            return None

        tree_interceptor = getattr(focus_obj, 'treeInterceptor', None)
        is_ti = bool(tree_interceptor and getattr(tree_interceptor, 'isAlive', False))
        root_obj = getattr(tree_interceptor, 'rootNVDAObject', None) if is_ti else None

        bookmark = None
        snippet = ""
        was_pass_through = False

        if is_ti:
            was_pass_through = getattr(tree_interceptor, 'passThrough', False)
            if not was_pass_through:
                # Browse Mode virtual buffer
                try:
                    info = getattr(tree_interceptor, 'selection', None)
                    if not info:
                        info = tree_interceptor.makeTextInfo(textInfos.POSITION_CARET)
                    if info:
                        bookmark = getattr(info, 'bookmark', None)
                        info_copy = info.copy()
                        info_copy.expand(textInfos.UNIT_LINE)
                        snippet = info_copy.text.strip()
                except Exception:
                    pass
            else:
                # Focus Mode inside a Browse Mode document
                try:
                    info = focus_obj.makeTextInfo(textInfos.POSITION_CARET)
                    bookmark = getattr(info, 'bookmark', None)
                    info_copy = info.copy()
                    info_copy.expand(textInfos.UNIT_LINE)
                    snippet = info_copy.text.strip()
                except Exception:
                    pass
                if not bookmark:
                    try:
                        info = getattr(tree_interceptor, 'selection', None)
                        if not info:
                            info = tree_interceptor.makeTextInfo(textInfos.POSITION_CARET)
                        if info:
                            bookmark = getattr(info, 'bookmark', None)
                    except Exception:
                        pass
        else:
            # Standard application control / document
            try:
                info = focus_obj.makeTextInfo(textInfos.POSITION_CARET)
                bookmark = getattr(info, 'bookmark', None)
                info_copy = info.copy()
                info_copy.expand(textInfos.UNIT_LINE)
                snippet = info_copy.text.strip()
            except Exception:
                pass

        # Fallback snippet
        if not snippet:
            try:
                name = getattr(focus_obj, 'name', '') or ''
                role = getattr(focus_obj.role, 'displayString', str(getattr(focus_obj, 'role', ''))) if hasattr(focus_obj, 'role') else ''
                snippet = f"{name} {role}".strip() or _("Control")
            except Exception:
                snippet = _("Control")

        # Application title
        app_name = ""
        try:
            app_name = focus_obj.appModule.appName if focus_obj.appModule else ""
        except Exception:
            app_name = ""

        name = custom_name if custom_name else _("Cursor {index}").format(index=index)

        return CursorPoint(
            index=index,
            name=name,
            app_name=app_name,
            obj=focus_obj,
            root_obj=root_obj,
            is_tree_interceptor=is_ti,
            tree_interceptor=tree_interceptor if is_ti else None,
            was_pass_through=was_pass_through,
            bookmark=bookmark,
            snippet=snippet
        )

    def set_cursor(self, index: int, announce: bool = True) -> bool:
        """Sets a specific cursor slot (1 to max_slots) to the current position."""
        if index < 1 or index > self.max_slots:
            return False

        point = self.capture_point(index)
        if not point:
            play_error_sound()
            if announce:
                ui.message(_("Could not save position."))
            return False

        self.cursors[index] = point
        self.previous_cursor_index = self.active_cursor_index
        self.active_cursor_index = index
        play_cursor_set_sound(index)

        if announce:
            preview = (point.snippet[:45] + "...") if len(point.snippet) > 45 else point.snippet
            app_info = f" ({point.app_name})" if point.app_name else ""
            ui.message(_("Cursor {index} saved{app}: {preview}").format(index=index, app=app_info, preview=preview))
        return True

    def add_next_cursor(self, announce: bool = True) -> Optional[int]:
        """Automatically saves current position to the next available slot."""
        # Find first empty slot
        target_slot = None
        for i in range(1, self.max_slots + 1):
            if self.cursors[i] is None:
                target_slot = i
                break

        # If all slots are full, overwrite the oldest non-active slot
        if target_slot is None:
            for i in range(1, self.max_slots + 1):
                if i != self.active_cursor_index:
                    target_slot = i
                    break

        if target_slot is None:
            target_slot = 1

        if self.set_cursor(target_slot, announce=announce):
            return target_slot
        return None

    def jump_to_cursor(self, index: int, announce: bool = True) -> bool:
        """Restores focus, virtual cursor, and caret to the specified cursor slot."""
        point = self.cursors.get(index)
        if not point:
            play_error_sound()
            if announce:
                ui.message(_("Cursor {index} is empty.").format(index=index))
            return False

        # Validate accessibility of target point
        if point.is_tree_interceptor:
            if not point.tree_interceptor or not getattr(point.tree_interceptor, 'isAlive', False):
                play_error_sound()
                if announce:
                    ui.message(_("Cursor {index} page is closed or reloaded.").format(index=index))
                return False
            # If the transient sub-element died, fallback to document root
            if not point.obj or not getattr(point.obj, 'isAlive', True):
                if point.root_obj and getattr(point.root_obj, 'isAlive', True):
                    point.obj = point.root_obj
        else:
            if not point.obj or not getattr(point.obj, 'isAlive', True):
                play_error_sound()
                if announce:
                    ui.message(_("Cursor {index} window is closed.").format(index=index))
                return False

        # Bring window to foreground if switching between windows
        try:
            import winUser
            hwnd = getattr(point.obj, 'windowHandle', None)
            if hwnd:
                fg = api.getForegroundObject()
                fg_hwnd = getattr(fg, 'windowHandle', None) if fg else None
                if fg_hwnd and hwnd != fg_hwnd:
                    winUser.setForegroundWindow(hwnd)
        except Exception:
            pass

        play_cursor_switch_sound(index)
        self.previous_cursor_index = self.active_cursor_index
        self.active_cursor_index = index

        restored_ok = False

        # 1. Browse mode virtual buffer restoration
        if point.is_tree_interceptor and point.tree_interceptor and getattr(point.tree_interceptor, 'isAlive', False):
            ti = point.tree_interceptor
            try:
                try:
                    point.obj.setFocus()
                    api.setFocusObject(point.obj)
                except Exception:
                    pass

                if point.was_pass_through:
                    ti.passThrough = True
                    if point.bookmark:
                        try:
                            info = point.obj.makeTextInfo(point.bookmark)
                            try:
                                info.updateCaret()
                            except Exception:
                                pass
                            if announce:
                                speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)
                        except Exception:
                            if announce:
                                speech.speakObject(point.obj, reason=controlTypes.OutputReason.FOCUS)
                else:
                    ti.passThrough = False
                    if point.bookmark:
                        try:
                            info = ti.makeTextInfo(point.bookmark)
                            ti.selection = info
                            try:
                                info.updateCaret()
                            except Exception:
                                pass
                            if announce:
                                speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)
                        except Exception:
                            pass
                    try:
                        api.setNavigatorObject(point.obj)
                    except Exception:
                        pass
                restored_ok = True
            except Exception:
                restored_ok = False

        # 2. Standard application control restoration
        if not restored_ok:
            try:
                point.obj.setFocus()
                api.setFocusObject(point.obj)
                api.setNavigatorObject(point.obj)
                if point.bookmark:
                    try:
                        info = point.obj.makeTextInfo(point.bookmark)
                        try:
                            info.updateCaret()
                        except Exception:
                            pass
                        if announce:
                            speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)
                    except Exception:
                        if announce:
                            speech.speakObject(point.obj, reason=controlTypes.OutputReason.FOCUS)
                else:
                    if announce:
                        speech.speakObject(point.obj, reason=controlTypes.OutputReason.FOCUS)
                restored_ok = True
            except Exception:
                restored_ok = False

        if not restored_ok:
            play_error_sound()
            if announce:
                ui.message(_("Unable to restore Cursor {index}").format(index=index))
            return False

        return True

    def get_active_indices(self) -> List[int]:
        """Returns sorted list of all currently populated cursor indices."""
        return [i for i, pt in self.cursors.items() if pt is not None]

    def cycle_cursor(self, forward: bool = True) -> bool:
        """Cycles to the next or previous active cursor."""
        active = self.get_active_indices()
        if not active:
            play_error_sound()
            ui.message(_("No saved cursors. Press NVDA+Shift+C to save your current position."))
            return False

        if len(active) == 1:
            play_cursor_switch_sound(active[0])
            ui.message(_("Only Cursor {slot} is saved. Press NVDA+Shift+C elsewhere to save a second place.").format(slot=active[0]))
            return True

        if self.active_cursor_index in active:
            curr_pos = active.index(self.active_cursor_index)
            next_pos = (curr_pos + 1) % len(active) if forward else (curr_pos - 1) % len(active)
            target = active[next_pos]
        else:
            target = active[0]

        play_cycle_sound(forward)
        return self.jump_to_cursor(target, announce=True)

    def toggle_recent(self) -> bool:
        """Toggles between the current cursor and the previously used cursor."""
        active = self.get_active_indices()
        if not active:
            play_error_sound()
            ui.message(_("No saved cursors. Press NVDA+Shift+C to save your current position."))
            return False

        if len(active) == 1:
            # If only 1 cursor exists, dropping a second one creates a pair ready to toggle
            second_slot = self.add_next_cursor(announce=False)
            if second_slot:
                ui.message(_("Cursor {slot} saved. Toggle pair ready!").format(slot=second_slot))
                return True
            return False

        # Pick the previous or alternate cursor
        target = self.previous_cursor_index
        if target == self.active_cursor_index or target not in active:
            for i in active:
                if i != self.active_cursor_index:
                    target = i
                    break

        return self.jump_to_cursor(target, announce=True)

    def delete_current_cursor(self) -> bool:
        """Deletes the active cursor."""
        idx = self.active_cursor_index
        if not self.cursors.get(idx):
            play_error_sound()
            ui.message(_("Cursor {index} is already empty.").format(index=idx))
            return False

        self.cursors[idx] = None
        play_cursor_delete_sound()
        ui.message(_("Cursor {index} removed.").format(index=idx))

        # Switch active index to another available cursor if any
        active = self.get_active_indices()
        if active:
            self.active_cursor_index = active[0]
        return True

    def clear_all(self):
        """Clears all cursors."""
        self.cursors = {i: None for i in range(1, self.max_slots + 1)}
        play_cursor_delete_sound()
        ui.message(_("All cursors cleared."))

    def peek_cursor(self, target_index: Optional[int] = None, direction: int = 0) -> bool:
        """
        Reads line text from a target cursor without moving current focus or typing caret.
        """
        active = self.get_active_indices()
        if not active:
            play_error_sound()
            ui.message(_("No saved cursors to peek."))
            return False

        if target_index is None:
            candidates = [i for i in active if i != self.active_cursor_index]
            target_index = candidates[0] if candidates else self.active_cursor_index

        pt = self.cursors.get(target_index)
        if not pt:
            play_error_sound()
            ui.message(_("Cursor {index} not found.").format(index=target_index))
            return False

        peek_info = pt.get_peek_info()
        if not peek_info:
            play_error_sound()
            ui.message(_("Cursor {index} text is not accessible.").format(index=target_index))
            return False

        try:
            if direction != 0:
                moved = peek_info.move(textInfos.UNIT_LINE, direction)
                if moved == 0:
                    play_error_sound()
                    if direction > 0:
                        ui.message(_("End of document"))
                    else:
                        ui.message(_("Top of document"))
                    return True

            line_info = peek_info.copy()
            line_info.expand(textInfos.UNIT_LINE)
            text = line_info.text.strip()

            play_peek_sound()
            if text:
                ui.message(text)
            else:
                ui.message(_("Blank line"))
            return True
        except Exception:
            play_error_sound()
            pt.reset_peek()
            ui.message(_("Unable to read line from Cursor {index}.").format(index=target_index))
            return False

    def list_cursors(self, prompt_dialog: bool = True):
        """Announces all active cursors with their positions and app names."""
        active = self.get_active_indices()
        if not active:
            ui.message(_("No saved cursors. Press NVDA+Shift+C to save your current position."))
            return

        summaries = []
        for i in active:
            pt = self.cursors[i]
            active_marker = _(" (Active)") if i == self.active_cursor_index else ""
            app_str = f" [{pt.app_name}]" if pt.app_name else ""
            preview = (pt.snippet[:30] + "..") if len(pt.snippet) > 30 else pt.snippet
            summaries.append(f"Cursor {i}{active_marker}{app_str}: {preview}")

        msg = f"{len(active)} cursors: " + "; ".join(summaries)
        if prompt_dialog:
            msg += _(". Press twice for Cursor Manager.")
        ui.message(msg)

    def open_manager_dialog(self):
        """Opens the interactive MultiFocus Cursor Manager dialog."""
        active = self.get_active_indices()
        if not active:
            play_error_sound()
            ui.message(_("No saved cursors. Press NVDA+Shift+C to save your current position."))
            return

        def run_dialog():
            import gui
            from .uiDialogs import MultiFocusDialog
            dlg = MultiFocusDialog(gui.mainFrame, self)
            result = gui.runScriptModalDialog(dlg)
            if result == wx.ID_OK and dlg.target_index is not None:
                import core
                core.callLater(50, self.jump_to_cursor, dlg.target_index, True)

        import core
        core.callLater(10, run_dialog)
