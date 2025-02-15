import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import configure_ipv6_acl


class TestConfigureIpv6Acl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Intrepid-DUT-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C9600
            type: C9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-DUT-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv6_acl(self):
        result = configure_ipv6_acl(
            device=self.device,
            acl_name='racl-1',
            service_type='tcp',
            src_nw='2013:1::20',
            dst_nw='2013:1::10',
            rule='permit',
            host_option=True,
            prefix='',
            dst_port='179',
            log_option='log',
            sequence_num='200')
        expected_output = None
        self.assertEqual(result, expected_output)
