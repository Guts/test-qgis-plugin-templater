#! python3  # noqa E265

"""
Usage from the repo root folder:

.. code-block:: bash

    # for whole tests
    python -m unittest tests.qgis.test_plg_processing
    # for specific test
    python -m unittest tests.qgis.test_plg_processing.TestPlgprocessing.test_plg_processing_structure
"""

# PyQGIS
from qgis.core import QgsApplication
from qgis.testing import unittest

from qgis_plugin_templater_test_github.processing.provider import (
    QgisPluginTemplaterTestGithubProvider,
)


class TestProcessing(unittest.TestCase):
    """Tests for processing algorithms."""

    def setUp(self) -> None:
        """Set up the processing tests."""
        if not QgsApplication.processingRegistry().providers():
            self.provider = QgisPluginTemplaterTestGithubProvider()
            QgsApplication.processingRegistry().addProvider(self.provider)
        self.maxDiff = None
