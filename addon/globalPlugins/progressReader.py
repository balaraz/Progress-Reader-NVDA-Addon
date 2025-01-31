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
    def __init__(self):
        super().__init__()

    def _findProgressBar(self):
        """Sucht nach einer Progressbar im aktiven Fenster (unterstützt UIA, IAccessible, wx.Gauge)."""
        q = Queue()
        root = api.getForegroundObject()
        q.put(root)

        while not q.empty():
            obj = q.get()
            
            try:
                # UIA (für moderne Windows-Anwendungen)
                if hasattr(obj, 'UIAElement') and obj.UIAElement:
                    if obj.UIAElement.controlType == UIAHandler.UIA_ControlTypeIds.PROGRESSBAR:
                        return obj

                # IAccessible (für klassische Windows-Anwendungen)
                if hasattr(obj, 'IAccessibleObject') and obj.IAccessibleObject:
                    if obj.IAccessibleObject.accRole(0) == controlTypes.Role.PROGRESSBAR:
                        return obj

                # NVDA Standard-Erkennung
                if obj.role == controlTypes.ROLE_PROGRESSBAR:
                    return obj

                # wx.Gauge (nur wenn explizit als Progressbar erkennbar)
                if hasattr(obj, "value") and hasattr(obj, "maxValue"):
                    return obj

                # Kinder zum Queue hinzufügen (nur falls vorhanden)
                for child in getattr(obj, 'children', []):
                    q.put(child)

            except Exception:
                continue  # Falls ein Objekt keine Kinder hat, einfach überspringen
                
        return None

    def _parseValue(self, value):
        """Konvertiert verschiedene Wertformate in numerische Werte."""
        try:
            if isinstance(value, str):
                match = re.search(r"(\d+\.?\d*)", value.replace(",", "."))
                return float(match.group(1)) if match else 0.0
            return float(value)
        except Exception:
            return 0.0

    @script(
        description=_("Liest den Fortschritt der Progressbar vor"),
        gesture="kb:NVDA+Shift+U"
    )
    def script_readProgress(self, gesture):
        try:
            progressBar = self._findProgressBar()
            
            if not progressBar:
                ui.message(_("Keine Progressbar gefunden"))
                return

            # Werte auslesen mit Fallbacks
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

            # Falls maxValue nicht ermittelt werden kann, setzen wir es auf 100
            if maxValue <= 0:
                maxValue = 100
            
            if current < 0:
                current = 0

            percent = (current / maxValue) * 100
            percent = max(0.0, min(100.0, percent))  # Begrenzung auf 0-100%

            # Status abfragen (falls verfügbar)
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

        except Exception as e:
            ui.message(_("Fehler beim Auslesen: {}").format(str(e)))
