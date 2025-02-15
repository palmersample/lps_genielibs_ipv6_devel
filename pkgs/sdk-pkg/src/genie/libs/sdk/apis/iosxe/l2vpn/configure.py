"""Common configure functions for bgp"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_l2vpn_storm_control(
    device, interface, service_instance_id, storm_control
):
    """ Configures storm control under service instance

        Args:
            device('obj'): device to configure
            interface('str'): interface name
            service_instance_id:('int'): service instance id
            storm_control('list'): list of storm control configurations
                ex.)
                        [
                            {
                                'traffic_flow': 'unicast',
                                'name': 'cir',
                                'val': 8000
                            },
                            {
                                'traffic_flow': 'broadcast',
                                'name': 'cir',
                                'val': 8000
                            },
                            {
                                'traffic_flow': 'multicast',
                                'name': 'cir',
                                'val': 8000
                            }
                        ]
        Returns:
            N/A
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring storm control under service "
        "instance: {} and interface: {}".format(service_instance_id, interface)
    )

    config = []
    config.append("interface {}\n".format(interface))

    config.append("service instance {} ethernet\n".format(service_instance_id))

    for sc in storm_control:
        traffic_flow = sc["traffic_flow"]
        name = sc["name"]
        val = sc["val"]

        config.append(
            "storm-control {} {} {}\n".format(traffic_flow, name, val)
        )
    try:
        device.configure("".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for storm control under service "
            "instance: {} and interface: {} with exception: {}".format(
                service_instance_id, interface, str(e)
            )
        )

def configure_l2vpn_vfi_context_vpls(device, vpn_id, pseudowire=None,auto_bgp=None):
    """
    Configures l2vpn vfi context vpls on device

    Args:
        device('obj'): device to configure
        vpn_id('str'): vpn_id to configure
        pseudowire('str', optional): pseudowire to configure,
                                     default value is None
        auto_bgp('bool',optional): to configured autodiscovery bgp singalling ldp

    Returns:
        N/A

    Raises:
        SubCommandFailure
    """
    log.info(
        "Configuring l2vpn vfi context vpls on {dev}".format(dev=device.name)
    )
    config = [
        "l2vpn vfi context vpls",
        "vpn id {vpn}".format(vpn=vpn_id)
    ]
    if pseudowire:
        for attr in pseudowire:
            config.append("member {attr}".format(attr=attr))
    if auto_bgp:
            config.append("autodiscovery bgp signaling ldp")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for l2vpn vfi vpls on "
            "{dev} with exception: {e}".format(
            dev=device.name, e=str(e)
            )
        )

def unconfigure_l2vpn_vfi_context_vpls(device):
    """
    Unconfigures l2vpn vfi context vpls on device

    Args:
        device('obj'): device to configure

    Returns:
        N/A

    Raises:
        SubCommandFailure
    """
    log.info(
        "Unconfiguring l2vpn vfi context vpls on {dev}".format(dev=device.name)
    )
    try:
        device.configure("no l2vpn vfi context vpls")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration removal failed for l2vpn vfi vpls on "
            "{dev} with exception: {e}".format(
            dev=device.name, e=str(e)
            )
        )

def configure_evpn_instance_vlan_based_flood_suppression(device, instance):
    """ Configuring l2vpn evpn instance vlan based flooding-suppression address-resolution disable
        Args:
            device ('obj'): Device object
            instance ('int'): instance number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = ["l2vpn evpn instance {} vlan-based".format(instance),
              "encapsulation vxlan",
              "flooding-suppression address-resolution disable"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error("Configuration failed for flooding-suppression address-resolution disable"
            "of instance: {} with exception:\n{}".format(instance, str(e))
        )

def unconfigure_evpn_instance_vlan_based_flood_suppression(device, instance):
    """ Un-Configuring l2vpn evpn instance vlan based flooding-suppression address-resolution disable
        Args:
            device ('obj'): Device object
            instance ('int'): instance number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = ["l2vpn evpn instance {} vlan-based".format(instance),
              "encapsulation vxlan",
              "no flooding-suppression address-resolution disable"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error("Failed to un-configure flooding-suppression address-resolution disable"
            "of instance: {} with exception:\n{}".format(instance, str(e))
        )
