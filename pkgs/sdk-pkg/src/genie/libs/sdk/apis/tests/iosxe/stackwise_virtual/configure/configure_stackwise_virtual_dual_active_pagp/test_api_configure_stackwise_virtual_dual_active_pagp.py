import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import configure_stackwise_virtual_dual_active_pagp


class TestConfigureStackwiseVirtualDualActivePagp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          farscape-pinfra-6:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: STARTREK
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['farscape-pinfra-6']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_stackwise_virtual_dual_active_pagp(self):
        result = configure_stackwise_virtual_dual_active_pagp(self.device, '1')
        expected_output = ('stackwise-virtual\r\n'
 'stackwise-virtual\r\n'
 'dual-active detection pagp\r\n'
 'Please reload the switch for Stackwise Virtual configuration to take '
 'effect\r\n'
 'dual-active detection pagp trust channel-group 1\r\n'
 'Upon reboot, the config will be part of running config but not part of start '
 'up config.\r\n')
        self.assertEqual(result, expected_output)
