import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.health.health import health_cpu


class TestHealthCpu(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R3_nx:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir mock_data --state connect
                protocol: unknown
            os: nxos
            platform: n9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R3_nx']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_health_cpu(self):
        result = health_cpu(self.device)
        expected_output = {'health_data': [{'process': 'ALL_PROCESSES', 'value': 18.31},
                 {'process': 'init', 'value': 0.0},
                 {'process': 'kthreadd', 'value': 0.0},
                 {'process': 'ksoftirqd/0', 'value': 0.0},
                 {'process': 'kworker/0:0H', 'value': 0.0},
                 {'process': 'rcu_sched', 'value': 0.0},
                 {'process': 'rcu_bh', 'value': 0.0},
                 {'process': 'migration/0', 'value': 0.0},
                 {'process': 'watchdog/0', 'value': 0.0},
                 {'process': 'watchdog/1', 'value': 0.0},
                 {'process': 'migration/1', 'value': 0.0},
                 {'process': 'ksoftirqd/1', 'value': 0.0},
                 {'process': 'kworker/1:0H', 'value': 0.0},
                 {'process': 'khelper', 'value': 0.0},
                 {'process': 'kdevtmpfs', 'value': 0.0},
                 {'process': 'netns', 'value': 0.0},
                 {'process': 'perf', 'value': 0.0},
                 {'process': 'khungtaskd', 'value': 0.0},
                 {'process': 'writeback', 'value': 0.0},
                 {'process': 'ksmd', 'value': 6.25},
                 {'process': 'crypto', 'value': 0.0},
                 {'process': 'kintegrityd', 'value': 0.0},
                 {'process': 'bioset', 'value': 0.0},
                 {'process': 'kblockd', 'value': 0.0},
                 {'process': 'ata_sff', 'value': 0.0},
                 {'process': 'edac-poller', 'value': 0.0},
                 {'process': 'rpciod', 'value': 0.0},
                 {'process': 'kworker/0:1', 'value': 0.0},
                 {'process': 'kworker/1:1', 'value': 0.0},
                 {'process': 'kswapd0', 'value': 0.0},
                 {'process': 'fsnotify_mark', 'value': 0.0},
                 {'process': 'nfsiod', 'value': 0.0},
                 {'process': 'acpi_thermal_pm', 'value': 0.0},
                 {'process': 'scsi_eh_0', 'value': 0.0},
                 {'process': 'scsi_tmf_0', 'value': 0.0},
                 {'process': 'scsi_eh_1', 'value': 0.0},
                 {'process': 'scsi_tmf_1', 'value': 0.0},
                 {'process': 'scsi_eh_2', 'value': 0.0},
                 {'process': 'scsi_tmf_2', 'value': 0.0},
                 {'process': 'scsi_eh_3', 'value': 0.0},
                 {'process': 'scsi_tmf_3', 'value': 0.0},
                 {'process': 'scsi_eh_4', 'value': 0.0},
                 {'process': 'scsi_tmf_4', 'value': 0.0},
                 {'process': 'scsi_eh_5', 'value': 0.0},
                 {'process': 'scsi_tmf_5', 'value': 0.0},
                 {'process': 'ipv6_addrconf', 'value': 0.0},
                 {'process': 'deferwq', 'value': 0.0},
                 {'process': 'kloopd0', 'value': 0.0},
                 {'process': 'aclqos', 'value': 0.0},
                 {'process': 'ptplc', 'value': 0.0},
                 {'process': 'monc', 'value': 0.0},
                 {'process': 'kworker/1:1H', 'value': 0.0},
                 {'process': 'scsi_eh_6', 'value': 0.0},
                 {'process': 'scsi_tmf_6', 'value': 0.0},
                 {'process': 'scsi_eh_7', 'value': 0.0},
                 {'process': 'scsi_tmf_7', 'value': 0.0},
                 {'process': 'kworker/0:2', 'value': 0.0},
                 {'process': 'kloopd10', 'value': 0.0},
                 {'process': 'jbd2/loop10-8', 'value': 0.0},
                 {'process': 'ext4-rsv-conver', 'value': 0.0},
                 {'process': 'libvirt_lxc', 'value': 0.0},
                 {'process': 'systemd', 'value': 0.0},
                 {'process': 'systemd-journal', 'value': 0.0},
                 {'process': 'systemd-logind', 'value': 0.0},
                 {'process': 'dbus-daemon', 'value': 0.0},
                 {'process': 'crond', 'value': 0.0},
                 {'process': 'agetty', 'value': 0.0},
                 {'process': 'sshd', 'value': 0.0},
                 {'process': 'kloopd1', 'value': 0.0},
                 {'process': 'kloopd2', 'value': 0.0},
                 {'process': 'kloopd3', 'value': 0.0},
                 {'process': 'kloopd4', 'value': 0.0},
                 {'process': 'kloopd5', 'value': 0.0},
                 {'process': 'kloopd6', 'value': 0.0},
                 {'process': 'kworker/0:1H', 'value': 0.0},
                 {'process': 'jbd2/sda4-8', 'value': 0.0},
                 {'process': 'trigger', 'value': 0.0},
                 {'process': 'jbd2/sda5-8', 'value': 0.0},
                 {'process': 'jbd2/sda6-8', 'value': 0.0},
                 {'process': 'wq_gnetlink0', 'value': 0.0},
                 {'process': 'jbd2/sda2-8', 'value': 0.0},
                 {'process': 'kworker/1:2', 'value': 0.0},
                 {'process': 'kloopd7', 'value': 0.0},
                 {'process': 'kloopd8', 'value': 0.0},
                 {'process': 'jbd2/sda3-8', 'value': 0.0},
                 {'process': 'jbd2/sda7-8', 'value': 0.0},
                 {'process': 'portmap', 'value': 0.0},
                 {'process': 'lockd', 'value': 0.0},
                 {'process': 'nfsd', 'value': 0.0},
                 {'process': 'rpc.mountd', 'value': 0.0},
                 {'process': 'rpc.statd', 'value': 0.0},
                 {'process': 'kloopd9', 'value': 0.0},
                 {'process': 'libvirtd_mon.sh', 'value': 0.0},
                 {'process': 'sh', 'value': 0.0},
                 {'process': 'sysmgr', 'value': 0.0},
                 {'process': 'libvirtd', 'value': 0.0},
                 {'process': 'inotifywait', 'value': 0.0},
                 {'process': 'kworker/u5:2', 'value': 0.0},
                 {'process': 'vsh.bin', 'value': 0.0},
                 {'process': 'kworker/u4:1', 'value': 0.0},
                 {'process': 'mping-thread', 'value': 0.0},
                 {'process': 'kworker/u5:1', 'value': 0.0},
                 {'process': 'kworker/u4:2', 'value': 0.0},
                 {'process': 'cctrl_kthread', 'value': 0.0},
                 {'process': 'kworker/u4:0', 'value': 0.0},
                 {'process': 'redun_kthread', 'value': 0.0},
                 {'process': 'usd_mts_kthread', 'value': 0.0},
                 {'process': 'ps', 'value': 0.0},
                 {'process': 'ls-notify-mts-t', 'value': 0.0},
                 {'process': 'sdwrapd', 'value': 0.0},
                 {'process': 'pfmclnt', 'value': 0.0},
                 {'process': 'xinetd', 'value': 0.0},
                 {'process': 'tftpd', 'value': 0.0},
                 {'process': 'dme_proxy', 'value': 0.0},
                 {'process': 'platform', 'value': 0.0},
                 {'process': 'dme_bootup_proxy', 'value': 0.0},
                 {'process': 'event_manager', 'value': 3.09},
                 {'process': 'policyelem', 'value': 0.0},
                 {'process': 'syslogd', 'value': 0.0},
                 {'process': 'vshd', 'value': 0.0},
                 {'process': 'template_manager', 'value': 0.0},
                 {'process': 'tamnw', 'value': 0.0},
                 {'process': 'smm', 'value': 0.0},
                 {'process': 'psshelper', 'value': 0.0},
                 {'process': 'pixm_vl', 'value': 0.0},
                 {'process': 'pixm_gl', 'value': 0.0},
                 {'process': 'nginx', 'value': 0.0},
                 {'process': 'mmode', 'value': 0.0},
                 {'process': 'lmgrd', 'value': 0.0},
                 {'process': 'fs-daemon', 'value': 0.0},
                 {'process': 'feature-mgr', 'value': 0.0},
                 {'process': 'confcheck', 'value': 0.0},
                 {'process': 'capability', 'value': 0.0},
                 {'process': 'bloggerd', 'value': 0.0},
                 {'process': 'psshelper_gsvc', 'value': 0.0},
                 {'process': 'tams_proc', 'value': 0.0},
                 {'process': 'clis', 'value': 0.0},
                 {'process': 'licmgr', 'value': 0.0},
                 {'process': 'cisco', 'value': 0.0},
                 {'process': 'tamd_proc', 'value': 0.0},
                 {'process': 'xmlma', 'value': 0.0},
                 {'process': 'vmm', 'value': 0.0},
                 {'process': 'vdc_mgr', 'value': 0.0},
                 {'process': 'usbhsd', 'value': 0.0},
                 {'process': 'ttyd', 'value': 0.0},
                 {'process': 'sysinfo', 'value': 0.0},
                 {'process': 'snmpmib_proc', 'value': 0.0},
                 {'process': 'sksd', 'value': 0.0},
                 {'process': 'res_mgr', 'value': 0.0},
                 {'process': 'plugin', 'value': 0.0},
                 {'process': 'plog_sup', 'value': 0.0},
                 {'process': 'patch-installer', 'value': 0.0},
                 {'process': 'nxapi', 'value': 0.0},
                 {'process': 'mvsh', 'value': 0.0},
                 {'process': 'mts_mgr', 'value': 0.0},
                 {'process': 'mping_server', 'value': 0.0},
                 {'process': 'module', 'value': 0.0},
                 {'process': 'kim', 'value': 0.0},
                 {'process': 'issu_helper', 'value': 0.0},
                 {'process': 'evms', 'value': 0.0},
                 {'process': 'epld_upgrade_stdby', 'value': 0.0},
                 {'process': 'diagclient', 'value': 0.0},
                 {'process': 'dhclient', 'value': 0.0},
                 {'process': 'crdcfg_server', 'value': 0.0},
                 {'process': 'core-dmon', 'value': 0.0},
                 {'process': 'confelem', 'value': 0.0},
                 {'process': 'clk_mgr', 'value': 0.0},
                 {'process': 'bios_daemon', 'value': 0.0},
                 {'process': 'ascii-cfg', 'value': 0.0},
                 {'process': 'klogd', 'value': 0.0},
                 {'process': 'securityd', 'value': 0.0},
                 {'process': 'cert_enroll', 'value': 0.0},
                 {'process': 'aaa', 'value': 0.0},
                 {'process': 'urib', 'value': 0.0},
                 {'process': 'obfl', 'value': 0.0},
                 {'process': 'aclmgr', 'value': 0.0},
                 {'process': 'evmc', 'value': 0.0},
                 {'process': 'ExceptionLog', 'value': 0.0},
                 {'process': 'bootvar', 'value': 0.0},
                 {'process': 'diagmgr', 'value': 0.0},
                 {'process': 'cardclient', 'value': 0.0},
                 {'process': 'device_test', 'value': 0.0},
                 {'process': 'ifmgr', 'value': 0.0},
                 {'process': 'xbar', 'value': 0.0},
                 {'process': 'l3vm', 'value': 0.0},
                 {'process': 'statsclient', 'value': 0.0},
                 {'process': 'npacl', 'value': 0.0},
                 {'process': 'adjmgr', 'value': 0.0},
                 {'process': 'u6rib', 'value': 0.0},
                 {'process': 'l2fwd', 'value': 0.0},
                 {'process': 'incrond', 'value': 0.0},
                 {'process': 'arp', 'value': 0.0},
                 {'process': 'icmpv6', 'value': 0.0},
                 {'process': 'pktmgr', 'value': 0.0},
                 {'process': 'netstack', 'value': 0.0},
                 {'process': 'radius', 'value': 0.0},
                 {'process': 'cdp', 'value': 0.0},
                 {'process': 'cfs', 'value': 0.0},
                 {'process': 'ip_dummy', 'value': 0.0},
                 {'process': 'ipv6_dummy', 'value': 0.0},
                 {'process': 'otm', 'value': 0.0},
                 {'process': 'snmpd', 'value': 0.0},
                 {'process': 'tcpudp_dummy', 'value': 0.0},
                 {'process': 'dcos-xinetd', 'value': 0.0},
                 {'process': 'callhome', 'value': 0.0},
                 {'process': 'port-profile', 'value': 0.0},
                 {'process': 'vman', 'value': 0.0},
                 {'process': 'spm', 'value': 0.0},
                 {'process': 'rpm', 'value': 0.0},
                 {'process': 'pltfm_config', 'value': 0.0},
                 {'process': 'plcmgr', 'value': 0.0},
                 {'process': 'pfstat', 'value': 0.0},
                 {'process': 'ntp', 'value': 0.0},
                 {'process': 'nbproxy', 'value': 0.0},
                 {'process': 'monitor', 'value': 0.0},
                 {'process': 'lldp', 'value': 0.0},
                 {'process': 'lim', 'value': 0.0},
                 {'process': 'l2rib', 'value': 0.0},
                 {'process': 'ipfib', 'value': 0.0},
                 {'process': 'igmp', 'value': 0.0},
                 {'process': 'eth_port_channel', 'value': 0.0},
                 {'process': 'ecp', 'value': 0.0},
                 {'process': 'adbm', 'value': 0.0},
                 {'process': 'acllog', 'value': 0.0},
                 {'process': 'eltm', 'value': 0.0},
                 {'process': 'ntpd', 'value': 0.0},
                 {'process': 'vlan_mgr', 'value': 0.0},
                 {'process': 'eth_dstats', 'value': 0.0},
                 {'process': 'ipqosmgr', 'value': 0.0},
                 {'process': 'lacp', 'value': 0.0},
                 {'process': 'diag_port_lb', 'value': 0.0},
                 {'process': 'ethpm', 'value': 0.0},
                 {'process': 'l2fm', 'value': 0.0},
                 {'process': 'stp', 'value': 0.0},
                 {'process': 'stripcl', 'value': 0.0},
                 {'process': 'copp', 'value': 0.0},
                 {'process': 'ufdm', 'value': 0.0},
                 {'process': 'u2', 'value': 0.0},
                 {'process': 'sal', 'value': 0.0},
                 {'process': 'mrib', 'value': 0.0},
                 {'process': 'mfdm', 'value': 0.0},
                 {'process': 'mcm', 'value': 0.0},
                 {'process': 'm6rib', 'value': 0.0},
                 {'process': 'l2pt', 'value': 0.0},
                 {'process': 'bgp', 'value': 0.0},
                 {'process': 'rip', 'value': 0.0},
                 {'process': 'ospfv3', 'value': 0.0},
                 {'process': 'ospf', 'value': 0.0},
                 {'process': 'isis', 'value': 0.0},
                 {'process': 'eigrp', 'value': 0.0},
                 {'process': 'm2rib', 'value': 0.0},
                 {'process': 'mcastfwd', 'value': 0.0},
                 {'process': 'msdp', 'value': 0.0},
                 {'process': 'pim', 'value': 0.0},
                 {'process': 'pim6', 'value': 0.0},
                 {'process': 'wdpunch_thread', 'value': 0.0},
                 {'process': 'bkncmd', 'value': 0.0},
                 {'process': 'bknevt', 'value': 0.0},
                 {'process': 'plog_lc', 'value': 0.0},
                 {'process': 'patch_installer', 'value': 0.0},
                 {'process': 'obfl_lc', 'value': 0.0},
                 {'process': 'dt_helper', 'value': 0.0},
                 {'process': 'crdclient', 'value': 0.0},
                 {'process': 't2usd', 'value': 0.0},
                 {'process': 'login', 'value': 0.0},
                 {'process': 'bfdc', 'value': 0.0},
                 {'process': 'iftmc', 'value': 0.0},
                 {'process': 'pixc', 'value': 0.0},
                 {'process': 'port_client', 'value': 0.0},
                 {'process': 'stats_client', 'value': 0.0},
                 {'process': 'mtm', 'value': 0.0}]}
        self.assertEqual(result, expected_output)
