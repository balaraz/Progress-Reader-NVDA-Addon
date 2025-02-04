# Copyright (C) 2024-2025 Imam Kahraman
# Released under GNU General Public License v3 (GPL-3.0)
# License File: https://www.gnu.org/licenses/gpl-3.0.txt
import globalPluginHandler
import ui
import api
from scriptHandler import script
import addonHandler
import controlTypes
import UIAHandler
from NVDAObjects import NVDAObject
from queue import Queue
import re

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""A global plugin for NVDA that reads the progress of progress bars."""

	def __init__(self):
		"""Initializes the global plugin."""
		super().__init__()
		# Define a category for the add-on in the input gestures dialog
		self.category = _("Progress Reader")

	def chooseGesture(self, gesture):
		"""
		Allows the user to change the gesture for the add-on in the input gestures dialog.
		"""
		# This method is called when the user wants to change the gesture for the add-on
		# We can simply return the gesture that was passed in, or modify it as needed
		return gesture

	def _parseValue(self, value):
		"""
		Converts various value formats into numeric values.

		Args:
			value (str, float, int): The value to be converted.

		Returns:
			float: The converted numeric value or 0.0 in case of an error.
		"""
		try:
			if isinstance(value, str):
				match = re.search(r"(\d+\.?\d*)", value.replace(",", "."))
				return float(match.group(1)) if match else 0.0
			return float(value)
		except Exception:
			return 0.0

	@script(
		description=_("Liest den Fortschritt der Progressbar vor"),
		gesture="kb:NVDA+Shift+U",
		category="Progress Reader"  # Assign the script to the "Progress Reader" category
	)
	def script_readProgress(self, gesture):
		"""
		Reads the progress of one or more progress bars.

		Args:
			gesture: The triggering gesture object.
		"""
		try:
			progressBars = self._findProgressBars()

			if not progressBars:
				ui.message(_("Keine Progressbar gefunden"))
				return

			if len(progressBars) == 1:
				progressBar, progressText = progressBars[0]
				if progressText:
					ui.message(progressText)
					return

				current = self._parseValue(
					getattr(progressBar, 'value',
							getattr(progressBar, 'IAccessibleObject', None) and
							getattr(progressBar.IAccessibleObject, 'accValue', lambda x: "0")(0) or
							0)
				)

				maxValue = self._parseValue(
					getattr(progressBar, 'maxValue',
							getattr(progressBar, 'IAccessibleObject', None) and
							getattr(progressBar.IAccessibleObject, 'accMaximum', lambda x: "100")(0) or
							100)
				)

				if maxValue <= 0:
					maxValue = 100

				if current < 0:
					current = 0

				percent = (current / maxValue) * 100
				percent = max(0.0, min(100.0, percent))

				status = ""
				if hasattr(progressBar, 'states'):
					if controlTypes.State.BUSY in progressBar.states:
						status = _(" (aktiv)")
					elif controlTypes.State.UNAVAILABLE in progressBar.states:
						status = _(" (inaktiv)")

				ui.message(_("{percent}% Fortschritt{status}").format(
					percent=round(percent, 1),
					status=status
				))
			else:
				messages = []
				for progressBar, progressText in progressBars:
					if progressText:
						messages.append(progressText)
						continue

					current = self._parseValue(
						getattr(progressBar, 'value',
								getattr(progressBar, 'IAccessibleObject', None) and
								getattr(progressBar.IAccessibleObject, 'accValue', lambda x: "0")(0) or
								0)
					)

					maxValue = self._parseValue(
						getattr(progressBar, 'maxValue',
								getattr(progressBar, 'IAccessibleObject', None) and
								getattr(progressBar.IAccessibleObject, 'accMaximum', lambda x: "100")(0) or
								100)
					)

					if maxValue <= 0:
						maxValue = 100

					if current < 0:
						current = 0

					percent = (current / maxValue) * 100
					percent = max(0.0, min(100.0, percent))

					status = ""
					if hasattr(progressBar, 'states'):
						if controlTypes.State.BUSY in progressBar.states:
							status = _(" (aktiv)")
						elif controlTypes.State.UNAVAILABLE in progressBar.states:
							status = _(" (inaktiv)")

					messages.append(_("{percent}% Fortschritt{status}").format(
						percent=round(percent, 1),
						status=status
					))

				if messages:
					ui.browseableMessage("\n".join(messages), isHtml=False)
				else:
					ui.message(_("Keine Progressbar gefunden"))

		except Exception as e:
			ui.message(_("Fehler beim Auslesen: {}").format(str(e)))

	def _findProgressBars(self):
		"""
		Searches for all progress bars in the active window.

		Returns:
			list: A list of tuples containing the found progress bar object and the progress text (if available).
		"""
		q = Queue()
		root = api.getForegroundObject()
		q.put(root)
		progressBars = []

		while not q.empty():
			obj = q.get()

			try:
				# 🟢 1. Windows copy operation: "OperationStatusWindow" in both views
				if obj.windowClassName == "OperationStatusWindow":
					# Read progress from the window name
					name = getattr(obj, 'name', '')
					if name and "%" in name:
						progressBars.append((obj, name))  # Add the object and progress text to the list

					# Search for a progress bar in the children
					for child in obj.children:
						# UIA detection for detailed view
						if hasattr(child, "UIAElement") and child.UIAElement:
							if child.UIAElement.controlType == UIAHandler.UIA_ControlTypeIds.PROGRESSBAR:
								if child.value is not None:  # 🔹 Only add if a value exists.
									progressBars.append((child, str(child.value)))

						# Fallback: IAccessible for compact view
						if hasattr(child, 'IAccessibleObject') and child.IAccessibleObject:
							if child.IAccessibleObject.accRole(0) == controlTypes.Role.PROGRESSBAR:
								val = child.IAccessibleObject.accValue(0)  # try for get value
								if val and "%" in val:
									progressBars.append((child, val))

				# 🟢 2. General UIA progress bars
				if hasattr(obj, 'UIAElement') and obj.UIAElement:
					if obj.UIAElement.controlType == UIAHandler.UIA_ControlTypeIds.PROGRESSBAR:
						if obj.value is not None:
							progressBars.append((obj, str(obj.value)))

				# 🟢 3. IAccessible progress bars
				if hasattr(obj, 'IAccessibleObject') and obj.IAccessibleObject:
					if obj.IAccessibleObject.accRole(0) == controlTypes.Role.PROGRESSBAR:
						val = obj.IAccessibleObject.accValue(0)
						if val and "%" in val:
							progressBars.append((obj, val))

				# 🟢 4. NVDA standard detection
				if obj.role == controlTypes.ROLE_PROGRESSBAR:
					if obj.value is not None:
						progressBars.append((obj, str(obj.value)))

				# 🟢 5. wx.Gauge (only if explicitly recognizable as a progress bar)
				if hasattr(obj, "value") and hasattr(obj, "maxValue"):
					if obj.value > 0:
						progressBars.append((obj, str(obj.value)))

				# 🔄 Add children to the queue (if available)
				for child in getattr(obj, 'children', []):
					q.put(child)

			except Exception:
				continue  # Skip if an object has no children

		return progressBars if progressBars else []

	def debug_UIA_tree(self):
		"""
		Outputs the UIA structure of the active window. A helper function for development.
		"""
		def traverse(obj, depth=0):
			indent = "  " * depth
			ui.message(f"{indent} - {obj.name} ({obj.role}) [{obj.windowClassName}]")
			for child in getattr(obj, 'children', []):
				traverse(child, depth + 1)

		root = api.getForegroundObject()
		traverse(root)