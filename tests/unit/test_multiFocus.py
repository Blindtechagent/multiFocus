# Copyright (C) 2026 NV Access Limited, Abdel, Pawan Kumar
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Unit tests for MultiFocus plugin and cursor manager."""

import sys
import unittest
from types import ModuleType
from unittest.mock import MagicMock


# Set up mocks for NVDA modules if not present in environment
def _setup_nvda_mocks():
	nvda_modules = [
		"globalPluginHandler",
		"addonHandler",
		"scriptHandler",
		"ui",
		"api",
		"textInfos",
		"controlTypes",
		"speech",
		"tones",
		"winUser",
		"wx",
		"gui",
		"gui.settingsDialogs",
		"gui.guiHelper",
		"config",
		"core",
	]
	for mod_name in nvda_modules:
		if mod_name not in sys.modules:
			mod = ModuleType(mod_name)
			sys.modules[mod_name] = mod

	# Specific mocks
	sys.modules["addonHandler"].initTranslation = MagicMock()

	# Config mock
	config_mod = sys.modules["config"]
	if not hasattr(config_mod, "conf"):
		class ConfigDict(dict):
			def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)
				self.spec = {}

		config_mod.conf = ConfigDict({
			"multiFocus": {
				"enabledByDefault": True,
			},
		})

	# GUI Settings dialogs mock
	sd_mod = sys.modules["gui.settingsDialogs"]
	if not hasattr(sd_mod, "SettingsPanel"):

		class MockSettingsPanel:
			def __init__(self, *args, **kwargs):
				pass

		class MockNVDASettingsDialog:
			categoryClasses = []

		sd_mod.SettingsPanel = MockSettingsPanel
		sd_mod.NVDASettingsDialog = MockNVDASettingsDialog
		sys.modules["gui"].settingsDialogs = sd_mod

	# GUI Helper mock
	gh_mod = sys.modules["gui.guiHelper"]
	if not hasattr(gh_mod, "BoxSizerHelper"):

		class MockBoxSizerHelper:
			def __init__(self, parent, sizer=None):
				pass

			def addItem(self, item):
				return item

		gh_mod.BoxSizerHelper = MockBoxSizerHelper
		sys.modules["gui"].guiHelper = gh_mod

	# wx CheckBox mock
	wx_mod = sys.modules["wx"]
	if not hasattr(wx_mod, "CheckBox"):

		class MockCheckBox:
			def __init__(self, parent, label=""):
				self._val = False
				self._label = label

			def SetValue(self, val):
				self._val = bool(val)

			def IsChecked(self):
				return self._val

		wx_mod.CheckBox = MockCheckBox

	def mock_script(category=None, description=None, gesture=None, gestures=None, *args, **kwargs):
		def decorator(func):
			func.category = category
			func.description = description
			all_gestures = []
			if gesture:
				all_gestures.append(gesture)
			if gestures:
				all_gestures.extend(gestures)
			func.gestures = all_gestures
			return func

		return decorator

	sys.modules["scriptHandler"].script = mock_script
	sys.modules["scriptHandler"].getLastScriptRepeatCount = MagicMock(return_value=0)

	class BaseGlobalPlugin:
		def __init__(self, *args, **kwargs):
			self._bound_gestures = {}
			self._gestureMap = self._bound_gestures

		def bindGesture(self, gestureIdentifier, scriptName):
			self._bound_gestures[gestureIdentifier] = scriptName

		def bindGestures(self, gestureMap):
			self._bound_gestures.update(gestureMap)

		def removeGestureBinding(self, gestureIdentifier):
			if gestureIdentifier in self._bound_gestures:
				del self._bound_gestures[gestureIdentifier]
			else:
				raise LookupError(f"Gesture not bound: {gestureIdentifier}")

		def clearGestureBindings(self):
			self._bound_gestures.clear()

		def terminate(self):
			pass

	sys.modules["globalPluginHandler"].GlobalPlugin = BaseGlobalPlugin
	sys.modules["ui"].message = MagicMock()
	sys.modules["tones"].beep = MagicMock()


_setup_nvda_mocks()

# Import multiFocus plugin, settings panel, and manager
from addon.globalPlugins.multiFocus import (
	GlobalPlugin,
	MultiFocusSettingsPanel,
	isEnabledByDefault,
	setEnabledByDefault,
)
from addon.globalPlugins.multiFocus.focusManager import MultiCursorManager
import gui.settingsDialogs


class TestMultiFocusDynamicMode(unittest.TestCase):
	"""Test case for verifying the dynamic MultiFocus mode, NVDA settings, and gesture binding/releasing."""

	def setUp(self):
		setEnabledByDefault(True)
		self.plugin = GlobalPlugin()

	def tearDown(self):
		self.plugin.terminate()
		setEnabledByDefault(True)

	def test_multifocus_on_by_default(self):
		"""MultiFocus must be enabled (ON) by default."""
		self.assertTrue(self.plugin.multifocusEnabled)

	def test_gestures_bound_when_on_by_default(self):
		"""When MultiFocus is ON by default, MultiFocus gestures must be bound."""
		for gesture, script_name in self.plugin.MULTIFOCUS_GESTURES.items():
			self.assertIn(
				gesture,
				self.plugin._bound_gestures,
				f"Gesture {gesture} should be bound by default when MultiFocus is ON",
			)
			self.assertEqual(self.plugin._bound_gestures[gesture], script_name)

	def test_mode_toggle_gesture_always_available(self):
		"""NVDA+Windows+M must be bound to toggleMultiFocusMode and always available."""
		gestures = getattr(self.plugin.script_toggleMultiFocusMode, "gestures", [])
		self.assertIn("kb:NVDA+windows+m", gestures)

	def test_gestures_released_when_toggled_off(self):
		"""When MultiFocus is toggled OFF, MultiFocus gestures must be released."""
		# MultiFocus is ON initially; toggling turns it OFF
		self.plugin.script_toggleMultiFocusMode(None)
		self.assertFalse(self.plugin.multifocusEnabled)

		for gesture in self.plugin.MULTIFOCUS_GESTURES:
			self.assertNotIn(
				gesture,
				self.plugin._bound_gestures,
				f"Gesture {gesture} should be released when MultiFocus is toggled OFF",
			)

	def test_gestures_bound_when_toggled_back_on(self):
		"""When MultiFocus is toggled back ON, MultiFocus gestures must be bound again."""
		# Turn OFF
		self.plugin.script_toggleMultiFocusMode(None)
		self.assertFalse(self.plugin.multifocusEnabled)

		# Turn back ON
		self.plugin.script_toggleMultiFocusMode(None)
		self.assertTrue(self.plugin.multifocusEnabled)

		for gesture, script_name in self.plugin.MULTIFOCUS_GESTURES.items():
			self.assertIn(
				gesture,
				self.plugin._bound_gestures,
				f"Gesture {gesture} should be rebound when MultiFocus is toggled ON",
			)
			self.assertEqual(self.plugin._bound_gestures[gesture], script_name)

	def test_plugin_termination_releases_bindings(self):
		"""Terminating the plugin must release all MultiFocus gesture bindings."""
		self.assertTrue(self.plugin.multifocusEnabled)
		self.plugin.terminate()

		for gesture in self.plugin.MULTIFOCUS_GESTURES:
			self.assertNotIn(
				gesture,
				self.plugin._bound_gestures,
				f"Gesture {gesture} should be released on plugin termination",
			)

	def test_no_nvda_alt_c_present(self):
		"""Verify that NVDA+Alt+C is completely absent from all gestures."""
		for gesture in self.plugin.MULTIFOCUS_GESTURES:
			self.assertNotIn("alt+c", gesture.lower())

		for attr_name in dir(self.plugin):
			if attr_name.startswith("script_"):
				func = getattr(self.plugin, attr_name)
				gestures = getattr(func, "gestures", [])
				for g in gestures:
					self.assertNotIn("alt+c", g.lower(), f"{attr_name} has alt+c gesture: {g}")

	def test_no_old_alt_numbers_present(self):
		"""Verify that NVDA+Alt+1..9 is completely absent from all gestures."""
		for gesture in self.plugin.MULTIFOCUS_GESTURES:
			for i in range(1, 10):
				self.assertNotIn(f"alt+{i}", gesture.lower())

	def test_final_gesture_scheme_dictionary(self):
		"""Verify every single required gesture exists in MULTIFOCUS_GESTURES."""
		expected = {
			"kb:NVDA+shift+c": "addCursor",
			"kb:NVDA+alt+f": "toggleRecent",
			"kb:NVDA+alt+rightArrow": "nextCursor",
			"kb:NVDA+alt+leftArrow": "previousCursor",
			"kb:NVDA+alt+l": "listCursors",
			"kb:NVDA+alt+h": "quickHelp",
			"kb:NVDA+alt+downArrow": "peekNext",
			"kb:NVDA+alt+upArrow": "peekPrevious",
			"kb:NVDA+alt+shift+c": "peekCurrent",
			"kb:NVDA+alt+delete": "deleteCurrent",
			"kb:NVDA+alt+shift+delete": "clearAll",
		}
		for gesture, script_name in expected.items():
			self.assertIn(gesture, self.plugin.MULTIFOCUS_GESTURES)
			self.assertEqual(self.plugin.MULTIFOCUS_GESTURES[gesture], script_name)

		for i in range(1, 10):
			self.assertEqual(self.plugin.MULTIFOCUS_GESTURES[f"kb:NVDA+shift+{i}"], f"setCursor{i}")
			self.assertEqual(self.plugin.MULTIFOCUS_GESTURES[f"kb:NVDA+control+{i}"], f"jumpCursor{i}")

	def test_disabling_multifocus_preserves_unrelated_gestures(self):
		"""Disabling MultiFocus must remove only MULTIFOCUS_GESTURES and preserve unrelated gestures."""
		unrelated_gesture = "kb:NVDA+control+shift+z"
		self.plugin.bindGesture(unrelated_gesture, "unrelatedAction")

		# MultiFocus is ON initially. Disable it.
		self.plugin.script_toggleMultiFocusMode(None)
		self.assertFalse(self.plugin.multifocusEnabled)

		# Unrelated gesture must still be present!
		self.assertIn(
			unrelated_gesture,
			self.plugin._bound_gestures,
			"Unrelated gesture was erroneously removed when MultiFocus was disabled!",
		)
		self.assertEqual(self.plugin._bound_gestures[unrelated_gesture], "unrelatedAction")

		# MultiFocus gestures must be removed
		for gesture in self.plugin.MULTIFOCUS_GESTURES:
			self.assertNotIn(gesture, self.plugin._bound_gestures)

	def test_termination_preserves_unrelated_gestures(self):
		"""Plugin termination must remove only MULTIFOCUS_GESTURES and preserve unrelated gestures."""
		unrelated_gesture = "kb:NVDA+control+shift+z"
		self.plugin.bindGesture(unrelated_gesture, "unrelatedAction")

		# Terminate
		self.plugin.terminate()

		# Unrelated gesture must still be present!
		self.assertIn(
			unrelated_gesture,
			self.plugin._bound_gestures,
			"Unrelated gesture was erroneously removed on termination!",
		)

		# MultiFocus gestures must be removed
		for gesture in self.plugin.MULTIFOCUS_GESTURES:
			self.assertNotIn(gesture, self.plugin._bound_gestures)

	def test_settings_panel_registration_and_unregistration(self):
		"""Verify MultiFocusSettingsPanel registers and unregisters cleanly."""
		self.assertIn(
			MultiFocusSettingsPanel,
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses,
		)
		self.plugin.terminate()
		self.assertNotIn(
			MultiFocusSettingsPanel,
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses,
		)

	def test_config_setting_controls_startup_state(self):
		"""Verify that when disabled in configuration, plugin loads with MultiFocus OFF."""
		setEnabledByDefault(False)
		self.assertFalse(isEnabledByDefault())

		off_plugin = GlobalPlugin()
		try:
			self.assertFalse(off_plugin.multifocusEnabled)
			for gesture in off_plugin.MULTIFOCUS_GESTURES:
				self.assertNotIn(
					gesture,
					off_plugin._bound_gestures,
					f"Gesture {gesture} should not be bound when startup setting is OFF",
				)
		finally:
			off_plugin.terminate()

	def test_settings_panel_makes_and_saves_settings(self):
		"""Verify that MultiFocusSettingsPanel creates controls and saves correctly."""
		panel = MultiFocusSettingsPanel()
		panel.makeSettings(None)
		self.assertTrue(panel.enabledByDefaultCheckBox.IsChecked())

		# Uncheck and save
		panel.enabledByDefaultCheckBox.SetValue(False)
		panel.onSave()
		self.assertFalse(isEnabledByDefault())

		# Check and save
		panel.enabledByDefaultCheckBox.SetValue(True)
		panel.onSave()
		self.assertTrue(isEnabledByDefault())


class TestMultiCursorManagerBasics(unittest.TestCase):
	"""Test MultiCursorManager basic slot management."""

	def setUp(self):
		self.mgr = MultiCursorManager(max_slots=9)

	def test_initial_state(self):
		self.assertEqual(len(self.mgr.cursors), 9)
		self.assertEqual(self.mgr.get_active_indices(), [])
		self.assertEqual(self.mgr.active_cursor_index, 1)

	def test_clear_all(self):
		self.mgr.cursors[1] = "dummy"
		self.mgr.cursors[2] = "dummy"
		self.assertEqual(len(self.mgr.get_active_indices()), 2)

		self.mgr.clear_all()
		self.assertEqual(self.mgr.get_active_indices(), [])
