# -*- coding: UTF-8 -*-
"""
Sound Effects module for MultiFocus (Multiple Cursors & Focuses).
Provides subtle, non-intrusive audio cues for adding, switching, cycling,
and deleting cursors without blocking NVDA's main thread.
"""

try:
    import tones
except ImportError:
    tones = None


def play_cursor_set_sound(index: int = 1):
    """Ascending chime confirming that a cursor has been created or set."""
    if not tones:
        return
    try:
        base = 440 + min(index, 9) * 40
        tones.beep(base, 25)
        tones.beep(int(base * 1.25), 35)
    except Exception:
        pass


def play_cursor_switch_sound(index: int = 1):
    """Two-tone chime indicating switch to a specific cursor."""
    if not tones:
        return
    try:
        freq = 380 + min(index, 9) * 55
        tones.beep(freq, 40)
    except Exception:
        pass


def play_cycle_sound(forward: bool = True):
    """Subtle chime when cycling through cursors."""
    if not tones:
        return
    try:
        if forward:
            tones.beep(520, 25)
            tones.beep(680, 30)
        else:
            tones.beep(680, 25)
            tones.beep(520, 30)
    except Exception:
        pass


def play_cursor_delete_sound():
    """Downward tone when a cursor is deleted or cleared."""
    if not tones:
        return
    try:
        tones.beep(500, 35)
        tones.beep(320, 45)
    except Exception:
        pass


def play_peek_sound():
    """Crisp high blip for peeking at another cursor's text."""
    if not tones:
        return
    try:
        tones.beep(988, 20)
    except Exception:
        pass


def play_error_sound():
    """Low tone indicating no cursor found or invalid target."""
    if not tones:
        return
    try:
        tones.beep(220, 50)
    except Exception:
        pass
