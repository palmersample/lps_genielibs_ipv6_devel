import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.isis.configure import configure_isis_network_type


class TestConfigureIsisNetworkType(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          mac-gen2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['mac-gen2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_isis_network_type(self):
        result = configure_isis_network_type(self.device, '49.0000.aaaa.aaaa.aaaa.00', 'level-1', 'all-interfaces', 'log-adjacency-changes')
        expected_output = None
        self.assertEqual(result, expected_output)
