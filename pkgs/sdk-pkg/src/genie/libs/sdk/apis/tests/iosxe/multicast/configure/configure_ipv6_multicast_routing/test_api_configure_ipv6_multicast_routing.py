import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_ipv6_multicast_routing


class TestConfigureIpv6MulticastRouting(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9300x-A:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300x-A']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv6_multicast_routing(self):
        result = configure_ipv6_multicast_routing(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
