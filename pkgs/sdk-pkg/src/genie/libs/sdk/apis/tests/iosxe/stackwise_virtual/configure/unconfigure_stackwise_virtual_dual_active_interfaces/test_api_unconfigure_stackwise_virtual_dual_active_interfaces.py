import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import unconfigure_stackwise_virtual_dual_active_interfaces


class TestUnconfigureStackwiseVirtualDualActiveInterfaces(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          farscape-pinfra-5:
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
        self.device = self.testbed.devices['farscape-pinfra-5']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_stackwise_virtual_dual_active_interfaces(self):
        result = unconfigure_stackwise_virtual_dual_active_interfaces(self.device, ['HundredGigE1/0/7'])
        expected_output = ('interface HundredGigE1/0/7\r\n'
        'interface HundredGigE1/0/7\r\n'
 'no stackwise-virtual dual-active-detection\r\n'
 'no stackwise-virtual dual-active-detection\r\n')
        self.assertEqual(result, expected_output)
