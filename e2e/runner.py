"""Run Behave against Django's live server and disposable test database."""

import os
import subprocess
import sys

from django.test import LiveServerTestCase


class CatalogBrowserTests(LiveServerTestCase):
    fixtures = ["sample_catalog"]

    def test_catalog_in_browser(self):
        subprocess.run(
            [sys.executable, "-m", "behave", "e2e/features"],
            env={**os.environ, "CATALOG_TEST_URL": self.live_server_url},
            check=True,
        )
