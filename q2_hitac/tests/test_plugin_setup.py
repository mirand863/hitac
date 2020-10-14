import unittest

from q2_hitac.plugin_setup import plugin as hitac_plugin


class PluginSetupTests(unittest.TestCase):

    def test_plugin_setup(self):
        self.assertEqual(emperor_plugin.name, 'hitac')
