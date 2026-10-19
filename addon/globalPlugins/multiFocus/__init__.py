# -*- coding: UTF-8 -*-
"""
MultiFocus Global Plugin for NVDA.
Provides multiple independent cursors and virtual focuses across any application,
web page, or document.
"""

import globalPluginHandler
import addonHandler
import scriptHandler
from scriptHandler import script
import ui

# Initialize translation support safely
try:
    addonHandler.initTranslation()
except Exception:
    pass

try:
    _ = _
except NameError:
    def _(msg):
        return msg

from .focusManager import MultiCursorManager

CATEGORY_NAME = _("MultiFocus (Multiple Cursors)")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """Global plugin providing multiple independent cursors & focus points for NVDA."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mgr = MultiCursorManager(max_slots=9)

    # --- Core Quick Workflow (Save, Toggle, Cycle) ---

    @script(
        category=CATEGORY_NAME,
        description=_("Saves a new cursor at your current position"),
        gesture="kb:NVDA+shift+c"
    )
    def script_addCursor(self, gesture):
        self.mgr.add_next_cursor()

    @script(
        category=CATEGORY_NAME,
        description=_("Toggles between your two most recent cursors"),
        gestures=["kb:NVDA+alt+c", "kb:NVDA+alt+f"]
    )
    def script_toggleRecent(self, gesture):
        self.mgr.toggle_recent()

    @script(
        category=CATEGORY_NAME,
        description=_("Cycles forward to the next active cursor"),
        gesture="kb:NVDA+alt+rightArrow"
    )
    def script_nextCursor(self, gesture):
        self.mgr.cycle_cursor(forward=True)

    @script(
        category=CATEGORY_NAME,
        description=_("Cycles backward to the previous active cursor"),
        gesture="kb:NVDA+alt+leftArrow"
    )
    def script_previousCursor(self, gesture):
        self.mgr.cycle_cursor(forward=False)

    # --- Interactive Manager & Quick Help ---

    @script(
        category=CATEGORY_NAME,
        description=_("Press once to announce active cursors; press twice to open Cursor Manager"),
        gesture="kb:NVDA+alt+l"
    )
    def script_listCursors(self, gesture):
        count = scriptHandler.getLastScriptRepeatCount()
        if count == 0:
            self.mgr.list_cursors(prompt_dialog=True)
        else:
            self.mgr.open_manager_dialog()

    @script(
        category=CATEGORY_NAME,
        description=_("Announces quick summary of MultiFocus shortcuts"),
        gesture="kb:NVDA+alt+h"
    )
    def script_quickHelp(self, gesture):
        ui.message(_(
            "MultiFocus Quick Guide: "
            "NVDA+Shift+C saves your cursor. "
            "NVDA+Alt+C toggles between recent cursors. "
            "NVDA+Alt+Right or Left Arrow cycles cursors. "
            "NVDA+Alt+L lists cursors, or press twice for Cursor Manager."
        ))

    # --- Audio Peek Commands (Inspect secondary cursor without moving focus) ---

    @script(
        category=CATEGORY_NAME,
        description=_("Peeks next line of alternate cursor without moving active focus"),
        gesture="kb:NVDA+alt+downArrow"
    )
    def script_peekNext(self, gesture):
        self.mgr.peek_cursor(direction=1)

    @script(
        category=CATEGORY_NAME,
        description=_("Peeks previous line of alternate cursor without moving active focus"),
        gesture="kb:NVDA+alt+upArrow"
    )
    def script_peekPrevious(self, gesture):
        self.mgr.peek_cursor(direction=-1)

    @script(
        category=CATEGORY_NAME,
        description=_("Peeks current line of alternate cursor without moving active focus"),
        gesture="kb:NVDA+alt+shift+c"
    )
    def script_peekCurrent(self, gesture):
        self.mgr.peek_cursor(direction=0)

    # --- Cursor Management ---

    @script(
        category=CATEGORY_NAME,
        description=_("Deletes the current active cursor"),
        gesture="kb:NVDA+alt+delete"
    )
    def script_deleteCurrent(self, gesture):
        self.mgr.delete_current_cursor()

    @script(
        category=CATEGORY_NAME,
        description=_("Clears all cursors"),
        gesture="kb:NVDA+alt+shift+delete"
    )
    def script_clearAll(self, gesture):
        self.mgr.clear_all()

    # --- Direct Numbered Slots (1 to 9) ---

    @script(category=CATEGORY_NAME, description=_("Sets Cursor 1 to current position"), gesture="kb:NVDA+shift+1")
    def script_setCursor1(self, gesture):
        self.mgr.set_cursor(1)

    @script(category=CATEGORY_NAME, description=_("Sets Cursor 2 to current position"), gesture="kb:NVDA+shift+2")
    def script_setCursor2(self, gesture):
        self.mgr.set_cursor(2)

    @script(category=CATEGORY_NAME, description=_("Sets Cursor 3 to current position"), gesture="kb:NVDA+shift+3")
    def script_setCursor3(self, gesture):
        self.mgr.set_cursor(3)

    @script(category=CATEGORY_NAME, description=_("Sets Cursor 4 to current position"), gesture="kb:NVDA+shift+4")
    def script_setCursor4(self, gesture):
        self.mgr.set_cursor(4)

    @script(category=CATEGORY_NAME, description=_("Sets Cursor 5 to current position"), gesture="kb:NVDA+shift+5")
    def script_setCursor5(self, gesture):
        self.mgr.set_cursor(5)

    @script(category=CATEGORY_NAME, description=_("Sets Cursor 6 to current position"), gesture="kb:NVDA+shift+6")
    def script_setCursor6(self, gesture):
        self.mgr.set_cursor(6)

    @script(category=CATEGORY_NAME, description=_("Sets Cursor 7 to current position"), gesture="kb:NVDA+shift+7")
    def script_setCursor7(self, gesture):
        self.mgr.set_cursor(7)

    @script(category=CATEGORY_NAME, description=_("Sets Cursor 8 to current position"), gesture="kb:NVDA+shift+8")
    def script_setCursor8(self, gesture):
        self.mgr.set_cursor(8)

    @script(category=CATEGORY_NAME, description=_("Sets Cursor 9 to current position"), gesture="kb:NVDA+shift+9")
    def script_setCursor9(self, gesture):
        self.mgr.set_cursor(9)

    @script(category=CATEGORY_NAME, description=_("Jumps to Cursor 1 and restores caret/focus"), gesture="kb:NVDA+alt+1")
    def script_jumpCursor1(self, gesture):
        self.mgr.jump_to_cursor(1)

    @script(category=CATEGORY_NAME, description=_("Jumps to Cursor 2 and restores caret/focus"), gesture="kb:NVDA+alt+2")
    def script_jumpCursor2(self, gesture):
        self.mgr.jump_to_cursor(2)

    @script(category=CATEGORY_NAME, description=_("Jumps to Cursor 3 and restores caret/focus"), gesture="kb:NVDA+alt+3")
    def script_jumpCursor3(self, gesture):
        self.mgr.jump_to_cursor(3)

    @script(category=CATEGORY_NAME, description=_("Jumps to Cursor 4 and restores caret/focus"), gesture="kb:NVDA+alt+4")
    def script_jumpCursor4(self, gesture):
        self.mgr.jump_to_cursor(4)

    @script(category=CATEGORY_NAME, description=_("Jumps to Cursor 5 and restores caret/focus"), gesture="kb:NVDA+alt+5")
    def script_jumpCursor5(self, gesture):
        self.mgr.jump_to_cursor(5)

    @script(category=CATEGORY_NAME, description=_("Jumps to Cursor 6 and restores caret/focus"), gesture="kb:NVDA+alt+6")
    def script_jumpCursor6(self, gesture):
        self.mgr.jump_to_cursor(6)

    @script(category=CATEGORY_NAME, description=_("Jumps to Cursor 7 and restores caret/focus"), gesture="kb:NVDA+alt+7")
    def script_jumpCursor7(self, gesture):
        self.mgr.jump_to_cursor(7)

    @script(category=CATEGORY_NAME, description=_("Jumps to Cursor 8 and restores caret/focus"), gesture="kb:NVDA+alt+8")
    def script_jumpCursor8(self, gesture):
        self.mgr.jump_to_cursor(8)

    @script(category=CATEGORY_NAME, description=_("Jumps to Cursor 9 and restores caret/focus"), gesture="kb:NVDA+alt+9")
    def script_jumpCursor9(self, gesture):
        self.mgr.jump_to_cursor(9)
