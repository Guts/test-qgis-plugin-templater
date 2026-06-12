#! python3  # noqa: E265

"""
Plugin settings form integrated into QGIS 'Options' menu.
"""

# standard
import platform
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import quote

# PyQGIS
from qgis.core import Qgis, QgsApplication
from qgis.gui import QgsOptionsPageWidget, QgsOptionsWidgetFactory
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtGui import QDesktopServices, QIcon
from qgis.PyQt.QtWidgets import QWidget

# project
from qgis_plugin_templater_test_github.__about__ import (
    __icon_path__,
    __title__,
    __uri_homepage__,
    __uri_tracker__,
    __version__,
)
from qgis_plugin_templater_test_github.toolbelt import PlgLogger, PlgOptionsManager
from qgis_plugin_templater_test_github.toolbelt.preferences import PlgSettingsStructure

if TYPE_CHECKING:
    from collections.abc import Callable

# ############################################################################
# ########## Classes ###############
# ##################################


class ConfigOptionsPage(QgsOptionsPageWidget):
    """Settings form embedded into QGIS 'options' menu."""

    def __init__(self, parent: QWidget) -> None:
        """Settings dialog constructor.

        :param QgsOptionsPageWidget parent: base class for widgets for pages included
            in the options dialog.
        """
        super().__init__(parent)
        self.log: Callable = PlgLogger().log
        self.plg_settings = PlgOptionsManager()

        # load UI and set objectName
        uic.loadUi(Path(__file__).parent / f"{Path(__file__).stem}.ui", self)
        self.setObjectName(f"mOptionsPage{__title__}")
        self.initGui()

    def initGui(self) -> None:  # noqa: N802
        """Set up UI elements."""
        # header
        report_context_message: str = quote(
            "> Reported from plugin settings\n\n"
            f"- operating system: {platform.system()} "
            f"{platform.release()}_{platform.version()}\n"
            f"- QGIS: {Qgis.QGIS_VERSION}\n"
            f"- plugin version: {__version__}\n"
        )

        # header
        self.lbl_title.setText(f"{__title__} - Version {__version__}")

        # customization
        self.btn_help.setIcon(QIcon(QgsApplication.iconPath("mActionHelpContents.svg")))
        self.btn_help.pressed.connect(
            partial(QDesktopServices.openUrl, QUrl(__uri_homepage__))
        )

        self.btn_report.setIcon(
            QIcon(QgsApplication.iconPath("console/iconSyntaxErrorConsole.svg"))
        )
        self.btn_report.pressed.connect(
            partial(
                QDesktopServices.openUrl,
                QUrl(
                    f"{__uri_tracker__}new/?"
                    "template=10_bug_report.yml"
                    f"&about-info={report_context_message}"
                ),
            )
        )

        self.btn_reset.setIcon(QIcon(QgsApplication.iconPath("mActionUndo.svg")))
        self.btn_reset.pressed.connect(self.on_reset_settings)

        # load previously saved settings
        self.load_settings()

    def apply(self) -> None:
        """Called to permanently apply the settings shown in the options page (e.g. \
        save them to QgsSettings objects). This is usually called when the options \
        dialog is accepted."""
        settings: PlgSettingsStructure = self.plg_settings.get_plg_settings()

        # misc
        settings.debug_mode = self.opt_debug.isChecked()
        settings.version = __version__

        # dump new settings into QgsSettings
        self.plg_settings.save_from_object(settings)

        if __debug__:
            self.log(
                message="DEBUG - Settings successfully saved.",
                log_level=Qgis.MessageLevel.NoLevel,
            )

    def load_settings(self) -> None:
        """Load options from QgsSettings into UI form."""
        settings: PlgSettingsStructure = self.plg_settings.get_plg_settings()

        # global
        self.opt_debug.setChecked(settings.debug_mode)
        self.lbl_version_saved_value.setText(settings.version)

    def on_reset_settings(self) -> None:
        """Reset settings to default values (set in preferences.py module)."""
        default_settings: PlgSettingsStructure = PlgSettingsStructure()

        # dump default settings into QgsSettings
        self.plg_settings.save_from_object(default_settings)

        # update the form
        self.load_settings()


class PlgOptionsFactory(QgsOptionsWidgetFactory):
    """Factory for options widget."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__()

    def icon(self) -> QIcon:
        """Returns plugin icon, used to as tab icon in QGIS options tab widget.

        :return: plugin's icon
        :rtype: QIcon
        """
        return QIcon(str(__icon_path__))

    def createWidget(self, parent: QWidget) -> ConfigOptionsPage:  # noqa: N802
        """Create settings widget.

        :param parent: Qt parent where to include the options page.
        :type parent: QObject

        :return: options page for tab widget
        :rtype: ConfigOptionsPage
        """
        return ConfigOptionsPage(parent)

    def title(self) -> str:
        """Returns plugin title, used to name the tab in QGIS options tab widget.

        :return: plugin title from about module
        :rtype: str
        """
        return __title__

    def helpId(self) -> str:  # noqa: N802
        """Returns plugin help URL.

        :return: plugin homepage url from about module
        :rtype: str
        """
        return __uri_homepage__
