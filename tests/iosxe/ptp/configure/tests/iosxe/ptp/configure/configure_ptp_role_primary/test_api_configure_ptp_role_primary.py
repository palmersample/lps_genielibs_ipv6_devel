import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ptp.configure import configure_ptp_role_primary


class TestConfigurePtpRolePrimary(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          centi_48TX_1:
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
        self.device = self.testbed.devices['centi_48TX_1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ptp_role_primary(self):
        result = configure_ptp_role_primary(self.device, ['te1/0/33'])
        expected_output = None
        self.assertEqual(result, expected_output)
