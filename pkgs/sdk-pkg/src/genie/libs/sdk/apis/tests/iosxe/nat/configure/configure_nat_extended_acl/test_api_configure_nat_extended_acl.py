import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_extended_acl


class TestConfigureNatExtendedAcl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Stargazer:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Stargazer']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_nat_extended_acl(self):
        result = configure_nat_extended_acl(self.device, 'acl_testing', 'permit', '172.16.0.0', '0.0.255.255', '198.16.0.0', '0.0.255.255')
        expected_output = None
        self.assertEqual(result, expected_output)
