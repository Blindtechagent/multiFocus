# -*- coding: UTF-8 -*-
"""
MultiFocus Cursor Manager Dialog for NVDA.
Provides an accessible, interactive dialog to browse, jump to, and delete cursors.
"""

import wx

try:
	_ = _
except NameError:

	def _(msg):
		return msg


class MultiFocusDialog(wx.Dialog):
	"""Accessible dialog to manage MultiFocus cursors."""

	def __init__(self, parent, mgr):
		super().__init__(
			parent,
			title=_("MultiFocus Cursor Manager"),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		self.mgr = mgr
		self.target_index = None

		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Guidance label
		lbl = wx.StaticText(
			self,
			label=_("&Saved Cursors (Press Enter to Jump, Delete to Remove):"),
		)
		main_sizer.Add(lbl, 0, wx.ALL, 10)

		# List box for cursors
		self.list_box = wx.ListBox(self, style=wx.LB_SINGLE)
		main_sizer.Add(self.list_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		# Action buttons
		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.btn_jump = wx.Button(self, label=_("&Jump To"))
		self.btn_jump.SetDefault()
		btn_sizer.Add(self.btn_jump, 0, wx.RIGHT, 6)

		self.btn_delete = wx.Button(self, label=_("&Delete"))
		btn_sizer.Add(self.btn_delete, 0, wx.RIGHT, 6)

		self.btn_clear = wx.Button(self, label=_("&Clear All"))
		btn_sizer.Add(self.btn_clear, 0, wx.RIGHT, 6)

		self.btn_close = wx.Button(self, wx.ID_CANCEL, label=_("&Close"))
		btn_sizer.Add(self.btn_close, 0)

		main_sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

		self.SetSizer(main_sizer)
		self.SetMinSize((500, 320))
		self.Fit()
		self.CenterOnParent()

		# Event bindings
		self.btn_jump.Bind(wx.EVT_BUTTON, self.on_jump)
		self.btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
		self.btn_clear.Bind(wx.EVT_BUTTON, self.on_clear)
		self.list_box.Bind(wx.EVT_LISTBOX_DCLICK, self.on_jump)
		self.list_box.Bind(wx.EVT_KEY_DOWN, self.on_list_key)

		self.refresh_list()
		self.list_box.SetFocus()

	def refresh_list(self):
		self.list_box.Clear()
		self.indices = self.mgr.get_active_indices()
		if not self.indices:
			self.EndModal(wx.ID_CANCEL)
			return

		selected_pos = 0
		for pos, slot in enumerate(self.indices):
			pt = self.mgr.cursors[slot]
			active_marker = _(" [Active]") if slot == self.mgr.active_cursor_index else ""
			app_str = f" ({pt.app_name})" if pt.app_name else ""
			preview = (pt.snippet[:40] + "..") if len(pt.snippet) > 40 else pt.snippet
			item_text = f"Cursor {slot}{active_marker}{app_str}: {preview}"
			self.list_box.Append(item_text)
			if slot == self.mgr.active_cursor_index:
				selected_pos = pos

		self.list_box.SetSelection(selected_pos)

	def on_list_key(self, event):
		key = event.GetKeyCode()
		if key == wx.WXK_DELETE:
			self.on_delete(None)
		elif key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			self.on_jump(None)
		else:
			event.Skip()

	def on_jump(self, event):
		sel = self.list_box.GetSelection()
		if sel != wx.NOT_FOUND and sel < len(self.indices):
			self.target_index = self.indices[sel]
			self.EndModal(wx.ID_OK)
		else:
			self.EndModal(wx.ID_CANCEL)

	def on_delete(self, event):
		sel = self.list_box.GetSelection()
		if sel != wx.NOT_FOUND and sel < len(self.indices):
			slot = self.indices[sel]
			self.mgr.cursors[slot] = None
			if self.mgr.active_cursor_index == slot:
				rem = self.mgr.get_active_indices()
				self.mgr.active_cursor_index = rem[0] if rem else 1
			self.refresh_list()

	def on_clear(self, event):
		self.mgr.clear_all()
		self.EndModal(wx.ID_CANCEL)
