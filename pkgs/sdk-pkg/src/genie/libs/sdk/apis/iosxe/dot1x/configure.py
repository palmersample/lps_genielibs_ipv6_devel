import logging
import re
from genie.libs.parser.utils.common import Common
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import (
    SubCommandFailure,
    StateMachineError,
    TimeoutError,
    ConnectionError,
)

log = logging.getLogger(__name__)

def source_configured_template(device, interface, template_name):
    """Source template config
        Args:
            device ('obj'): device to use
            interface (`str`): Interface name
            template (`str`): Built-in/User defined template Name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to source a configured template
    """
    converted_interface = Common.convert_intf_name(interface)
    cmd = ''
    cmd += 'interface {}\n'.format(converted_interface)
    cmd += 'source template {}'.format(template_name)
    log.info("Assign template {tmp} on {intf}".format(tmp=template_name, intf=converted_interface))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not source a configured template {}.Error: {}".format(template_name, str(e))
        )

def configure_dot1x_cred_profile(device, profile_name, user_name, passwd, passwd_type=None):
    """Configure EAP Md5 profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): dot1x credential profile name
            username (`str`): username for dot1x user
            passwd (`str`): password in plain text
            passwd_type('str',optional): password type (HIDDEN/UNENCRYPTED),defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure dot1x credential
    """
    cmd = ''
    cmd += 'dot1x credentials {}\n'.format(profile_name)
    cmd += 'username {}\n'.format(user_name)
    if passwd_type == 'HIDDEN':
        cmd += 'password 7 {}\n'.format(passwd)
    elif passwd_type == 'UNENCRYPTED':
        cmd += 'password 0 {}\n'.format(passwd)
    else:
        cmd += 'password {}\n'.format(passwd)
    #cmd += 'password {}\n'.format(passwd)
    log.info("configure dot1x credential")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure dot1x credential profile {}.Error: {}".format(profile_name, str(e))
        )

def configure_eap_profile(device, profile_name,method='md5'):
    """Configure EAP Md5 profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): eap profile name
            method ('str',optional). Method to use for eap authentication. Default is md5
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure eap md5 profile
    """
    cmd = ''
    cmd += 'eap profile {}\n'.format(profile_name)
    cmd += 'method {}\n'.format(method)
    log.debug("Configure eap profile")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure eap profile {}.Error: {}".format(profile_name, str(e))
        )

def unconfigure_eap_profile(device, profile_name):
    """Unconfigure EAP Profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): eap profile name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure eap md5 profile
    """
    cmd = 'no eap profile {}\n'.format(profile_name)
    log.info("Unconfigure eap profile {}".format(profile_name))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure profile: {profile_name}".format(profile_name=profile_name)
        )

def configure_eap_profile_md5(device, profile_name):
    """Configure EAP Md5 profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): eap profile name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure eap md5 profile
    """
    cmd = ''
    cmd += 'eap profile {}\n'.format(profile_name)
    cmd += 'method md5\n'
    log.info("configure eap md5 profile")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure eap md5 profile {}.Error: {}".format(profile_name, str(e))
        )

def configure_dot1x_supplicant(device, interface, cred_profile_name=None, eap_profile=None,auth_port_control=None):
    """Configure switch as dot1x supplicant/client
    Args:
        device ('obj'): device to use
        interface (`str`): Interface name
        cred_profile_name (`str`,optional): dot1x credential profile name
        eap_profile (`str`, optional): eap profile name (Default is None)
        auth_port_control ('str',optional): Port control type (i.e auto, force-authorized)
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure eap md5 profile
    """
    converted_interface = Common.convert_intf_name(interface)
    cmd = ''
    cmd += 'interface {}\n'.format(converted_interface)
    cmd += 'dot1x pae supplicant\n'

    if cred_profile_name:
        cmd += 'dot1x credentials {cred_profile_name}\n'.format(cred_profile_name=cred_profile_name)

    if eap_profile is not None:
        cmd += 'dot1x supplicant eap profile {}\n'.format(eap_profile)

    if auth_port_control:
        cmd += 'authentication port-control {auth_port_control}\n'.format(auth_port_control=auth_port_control)

    log.info("configure dot1x supplicant")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure dot1x_supplicant on {}.Error: {}".format(converted_interface, str(e))
        )

def configure_mode_to_eEdge(device):
    """ Convert the configuration mode to eEdge
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Convert the configuration mode to eEdge
    """
    cmd = 'authentication convert-to new-style forced'
    out = device.execute('authentication display config-mode')
    matchout = re.search('legacy',out)
    if matchout is not None:
        log.info("convert-to new-style")
        try:
             device.configure(cmd)
        except SubCommandFailure as e:
             raise SubCommandFailure(
                 "Failed to Convert the configuration mode to eEdge monitor.Error: {}".format(str(e))
            )
    else:
        log.info('switch is already configured in new-style')

def enable_autoconf(device):
    """ Enable autoconf
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable autoconf
    """
    out = device.execute('authentication display config-mode')
    matchout = re.search('legacy', out)
    if matchout is not None:
        log.info('Switch is in legacy mode, converting to new-style')
        cmd = ''
        cmd += 'authentication convert-to new-style forced\n'
        cmd += 'autoconf enable\n'
    else:
        cmd = ''
        cmd += 'autoconf enable\n'

    log.info("Enable autoconf")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to enable autoconf.Error: {}".format(str(e))
        )

def configure_access_session_monitor(device):
    """ Enable access-session  monitor
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable access-session monitor
    """
    out = device.execute('authentication display config-mode')
    matchout = re.search('legacy', out)
    if matchout is not None:
        log.info('Switch is in legacy mode, converting to new-style')
        cmd = ''
        cmd += 'authentication convert-to new-style forced\n'
        cmd += 'access-session monitor\n'
    else:
        cmd = ''
        cmd += 'access-session monitor\n'

    log.info("Configure access-session monitor")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to enable access-session monitor.Error: {}".format(str(e))
        )

def configure_access_session_sticky(device, timer):
    """ configure interface-template sticky timer
        Args:
            device ('obj'): device to use
            timer (int): <1-65535>  Enter a value between 1 and 65535
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure interface-template sticky timer
    """
    out = device.execute('authentication display config-mode')
    matchout = re.search('legacy', out)
    if matchout is not None:
        log.info('Switch is in legacy mode, converting to new-style')
        cmd = ''
        cmd += 'authentication convert-to new-style forced\n'
        cmd += 'access-session interface-template sticky timer {}\n'.format(timer)
    else:
        cmd = ''
        cmd += 'access-session interface-template sticky timer {}\n'.format(timer)

    log.info("Configure interface-template sticky timer")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure access-session sticky timer on {}.Error: {}".format(timer, str(e))
        )

def enable_dot1x_sysauthcontrol(device):
    """ Globally enables 802.1X port-based authentication.
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable 802.1X port-based authentication.
    """
    log.info("Enables 802.1X port-based authentication")
    cmd = ""
    cmd += "dot1x system-auth-control\n"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to enable dot1x system auth-control.Error: {}".format(str(e))
        )

def clear_access_session(device, interface=None):
    """ executes clear access-sesssion CLI
        Args:
            device ('obj'): device to use
            interface (`str`): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to execute clear access-sesssion.
    """
    converted_interface = Common.convert_intf_name(interface)
    cmd = "clear access-session"

    if interface:
        cmd += " interface {intf}".format(intf=converted_interface)

    cmd += "\n"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to execute clear access-sesssion.Error: {}".format(str(e))
        )


def config_identity_ibns(device, policy_map, interface=None, access=True, port_control='auto', template_name=None, **kwargs):
    """ Configure 802.1x port based authentication for
        IBNS2.0 with service policy under interface/template
    Mandatory args:
            device ('obj'): device to use
            access ('bol'): Set to True, False to configure in Trunk mode
            policy_map('str'): Name of policy map to be attached.
    Optional args:
        interface (`str`,optional): Interface name
        data_vlan(`int`): vlan_id for data traffic
        voice_vlan(`int`): vlan_id for voice traffic
        max_req:(`int`) Max No. of Retries
        max_reauth_req(`int`): Max No. of Reauthentication Attempts
        authmod('str'): default(multi-auth), mult-host peer, multi-domain etc
        closed('bol'):  {False: closed | True: open (default) }
        open('bol'): {False: closed | True: open (default) }
        reauth('str'):  server or numberic range is 1 to 65535 seconds
        ctr('str'): {both | in}
        txp(`int`):The range is 1 to 65535 seconds
        port_control ('str'): {auto|force-authorized|force-unauthorized}. Default = 'auto'
        template_name ('str'): Template name to be configured
        txp_sup ('int'): The range is 1 to 65535 seconds
    Returns:
            None
    Raises:
            SubCommandFailure: Failed to configure 802.1x port based authentication
    """
    dict1 = {}
    #For IBNS2.0  access-session is in Open mode (default)
    #dict1['open'] = True
    #For IBNS2.0 default access-session host-mode is in multi-auth (default)
    dict1['authmod'] ='multi-auth'

    cmd = " "
    if interface is not None:
        converted_interface = Common.convert_intf_name(interface)
        cmd += 'interface {}\n'.format(converted_interface)
    else:
        cmd += f'template {template_name}\n'

    if access:
        if template_name is None:
            cmd += "switchport\n"
            cmd += "switchport mode access\n"
        else:
            cmd += "switchport mode access\n"
    else:
        if template_name is None:
            cmd += "switchport\n"
            cmd += "switchport mode trunk\n"
        else:
            cmd += "switchport mode trunk\n"

    cmd += "access-session port-control {port_control}\n".format(port_control=port_control)
    cmd += "authentication periodic\n"
    cmd += "mab\n"
    cmd += "dot1x pae authenticator\n"

    for key, value in kwargs.items():
        if type(value) == str:
            dict1[key] = value.lower()
        else:
            dict1[key] = value

    if 'data_vlan' in dict1:
       cmd += "switchport access vlan {}\n".format(dict1['data_vlan'])

    if 'voice_vlan' in dict1:
       cmd += "switchport voice vlan {}\n".format(dict1['voice_vlan'])

    if 'max_req'in dict1:
        cmd += "dot1x max-req {}\n".format(dict1['max_req'])

    if 'max_reauth_req'in dict1:
        cmd += "dot1x max-reauth-req {}\n".format(dict1['max_reauth_req'])

    if  'txp' in dict1:
        cmd += "dot1x timeout tx-period {}\n".format(dict1['txp'])

    if 'txp_sup' in dict1 :
        cmd += f"dot1x timeout supp-timeout {dict1['txp_sup']}\n"

    if dict1['authmod'] != 'multi-auth':
        cmd += "access-session host-mode {}\n".format(dict1['authmod'])

    if dict1['open'] == False:
        cmd += "access-session closed\n"

    if 'ctr' in dict1:
        cmd += "access-session control-direction {}\n".format(dict1['ctr'])

    if  'reauth' in dict1:
        cmd += "authentication timer reauthenticate {}\n".format(dict1['reauth'])

    cmd += "service-policy type control subscriber {}\n".format(policy_map)

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure 802.1x port based Authentication on {}"
            "Error: {}".format(converted_interface, str(e))
        )


def unconfigure_dot1x_cred_profile(device, profile_name):
    """Unconfigure dot1x credentials profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): dot1x credential profile name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure dot1x credential
    """
    cmd = 'no dot1x credentials {}\n'.format(profile_name)
    log.info("unconfigure dot1x credential")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure dot1x credential profile {}.Error: {}".format(profile_name, str(e))
        )


def unconfigure_eap_profile_md5(device, profile_name):
    """Configure EAP Md5 profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): eap profile name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure eap md5 profile
    """
    cmd = 'no eap profile {}\n'.format(profile_name)
    log.info("unconfigure eap md5 profile")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure eap md5 profile {}.Error: {}".format(profile_name, str(e))
        )

def unconfigure_access_session_monitor(device):
    """ Enable access-session  monitor
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable access-session monitor
    """
    cmd = 'no access-session monitor\n'
    log.info("Unconfigure access-session monitor")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to disable access-session monitor.Error: {}".format(str(e))
        )


def unconfigure_access_session_sticky(device, timer):
    """ configure interface-template sticky timer
        Args:
            device ('obj'): device to use
            timer (int): <1-65535>  Enter a value between 1 and 65535
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure interface-template sticky timer
    """
    cmd = 'no access-session interface-template sticky timer {}\n'.format(timer)
    log.info("Unconfigure interface-template sticky timer")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure access-session sticky timer on {}.Error: {}".format(timer, str(e))
        )


def disable_dot1x_sysauthcontrol(device):
    """ Globally disables 802.1X port-based authentication.
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to disable 802.1X port-based authentication.
    """
    log.info("Disables 802.1X port-based authentication")
    cmd = "no dot1x system-auth-control\n"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to Disablele dot1x system auth-control.Error: {}".format(str(e))
        )


def unconfigure_dot1x_supplicant(device, profile_name, intf, eap_profile=None):

    """ UnConfigure on dot1x supplicant switch
    Args:
        device (`obj`): Device object
        profile_name (`str`): dot1x Credential profile_name
        intf (`str`) : Supplicant Interface
        eap_profile (`str`, optional): eap profile name (Default is None)
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    config_list = []
    config_list.append("no dot1x credentials {}".format(profile_name))
    config_list.append("interface {}".format(intf))
    config_list.append("no dot1x pae supplicant")

    if eap_profile is not None:
        config_list.append("no dot1x supplicant eap profile {}".format(eap_profile))

    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure dot1x supplicant username {profile_name}\
            on pagent interface {intf}'.format(profile_name=profile_name,intf=intf)
        )

def unconfigure_dot1x_system_auth_control(device):

    """UnConfigure dot1x system-auth-control
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no dot1x system-auth-control"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure dot1x system-auth-control'
        )

def configure_authentication_host_mode(device, mode, intf, style='legacy'):

    """Configure legacy cli authentication host-mode multi-auth/multi-domain/multi-host/single-host
    Args:
        device (`obj`): Device object
        mode (`str`): Host mode
        intf (`str`): Interface to configure
        style (`str`, optional): legacy or new (Default is legacy)
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = ""
    if style == "new":
        cmd = "access-session"
    else:
        cmd = "authentication"
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "{cmd} host-mode {mode}".format(cmd=cmd,mode=mode)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to configure host-mode'
    )

def unconfigure_authentication_host_mode(device,mode,intf,style='legacy'):

    """UnConfigure legacy cli authentication host-mode multi-auth/multi-domain/multi-host/single-host
    Args:
        device (`obj`): Device object
        mode (`str`): Host mode
        intf (`str`): Interface to configure
        style (`str`, optional): legacy or new (Default is legacy)
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = ""
    if style == "new":
        cmd = "access-session"
    else:
        cmd = "authentication"

    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no {cmd} host-mode {mode}".format(cmd=cmd,mode=mode)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure host-mode'
        )

def configure_authentication_order(device,order,intf):

    """Configure legacy cli authentication order dot1x/mab/webauth
    Args:
        device (`obj`): Device object
        order (`str`): mab dot1x/dot1x/mab/dot1x mab
        intf (`str`): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "authentication order {order}".format(order=order)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to configure authentication order'
        )

def unconfigure_authentication_order(device,order,intf):

    """UnConfigure legacy cli authentication order dot1x/mab/webauth
    Args:
        device (`obj`): Device object
        order (`str`): mab dot1x/dot1x/mab/dot1x mab
        intf (`str`): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no authentication order {order}".format(order=order)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication order'
    )

def configure_authentication_priority(device,priority,intf):

    """Configure legacy cli authentication priority dot1x/mab/webauth
    Args:
        device (`obj`): Device object
        priority (`str`): mab dot1x/dot1x/mab/dot1x mab
        intf (`str`): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "authentication priority {priority}".format(priority=priority)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to configure authentication priority'
        )

def unconfigure_authentication_priority(device,priority,intf):

    """Unconfigure legacy cli authentication priority dot1x/mab/webauth
    Args:
        device (`obj`): Device object
        priority (`str`): mab dot1x/dot1x/mab/dot1x mab
        intf (`str`): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no authentication priority {priority}".format(priority=priority)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication priority'
        )

def configure_authentication_port_control(device,control,intf,style='legacy'):

    """Configure legacy cli
    authentication port-control auto/force-authorized/force-unauthorized
    Args:
        device (`obj`): Device object
        control (`str`): auto/force-authorized/force-unauthorized
        intf (`str`): Interface to configure
        style (`str`, optional): legacy or new (Default is legacy)
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """

    cmd = ""
    if style == "new":
        cmd = "access-session"
    else:
        cmd = "authentication"

    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "{cmd} port-control {control}".format(cmd=cmd,control=control)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to configure authentication port-control'
        )

def unconfigure_authentication_port_control(device,control,intf,style='legacy'):

    """UnConfigure legacy cli
    authentication port-control auto/force-authorized/force-unauthorized
    Args:
        device (`obj`): Device object
        control (`str`): auto/force-authorized/force-unauthorized
        intf (`str`): Interface to configure
        style (`str`, optional): legacy or new (default is legacy)
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = ""
    if style == "new":
        cmd = "access-session"
    else:
        cmd = "authentication"
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no {cmd} port-control {control}".format(cmd=cmd,control=control)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication port-control'
        )

def configure_authentication_periodic(device,intf):

    """Configure legacy cli
        authentication periodic
    Args:
        device (`obj`): Device object
        intf (`str`): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "authentication periodic"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to configure authentication periodic'
)

def unconfigure_authentication_periodic(device,intf):

    """UnConfigure legacy cli
    authentication periodic
    Args:
        device (`obj`): Device object
        intf (`str`): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no authentication periodic"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication periodic'
)

def configure_authentication_timer_reauth(device,value,intf):

    """Configure legacy cli
    authentication timer reauthenticate value/server
    Args:
        device (`obj`): Device object
        value (`str`): authentication timer reauthenticate value/server
        intf (`str`): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "authentication timer reauthenticate {value}".format(value=value)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication timer reauthenticate'
        )

def unconfigure_authentication_timer_reauth(device,intf):

    """UnConfigure legacy cli
    authentication timer reauthenticate value/server
    Args:
        device (`obj`): Device object
        intf (`str`): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no authentication timer reauthenticate"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication timer reauthenticate'
    )

def configure_auth_method(device,value,intf):

    """Configure cli
    authentication method mab/dot1x pae authenticator
    Args:
        device (`obj`): Device object
        value (`str`): mab/dot1x
        intf (`str`): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = ""
    if value == "dot1x":
        cmd = "dot1x pae authenticator"
    elif value == "mab":
        cmd = "mab"
    else:
        cmd = value

    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "{cmd}".format(cmd=cmd)
        ])
    except SubCommandFailure:
        log.error('Failed configuring authentication method')

def unconfigure_auth_method(device,value,intf):

    """unconfigure legacy cli
    authentication method mab/dot1x pae authenticator
    Args:
        device (`obj`): Device object
        value (`str`): mab/dot1x
        intf (`str`): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = ""
    if value == "dot1x":
        cmd = "dot1x pae authenticator"
    elif value == "mab":
        cmd = "mab"
    else:
        cmd = value

    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no {cmd}".format(cmd=cmd)
        ])
    except SubCommandFailure:
        log.error('Failed unconfiguring authentication method')

def configure_dot1x_cred_pki(device, profile_name, user_name, pki_trustpoint):
    """Configure EAP Md5 profile with PKI
        Args:
            device ('obj'): device to use
            profile_name (`str`): dot1x credential profile name
            username (`str`): username for dot1x user
            pki_trustpoint (`str`): PKI trustpoint name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure dot1x credential
    """
    cmd = ''
    cmd += f'dot1x credentials {profile_name}\n'
    cmd += f'username {user_name}\n'
    cmd += f'pki-trustpoint {pki_trustpoint}\n'

    log.info("Configure dot1x credential with PKI")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure dot1x credential profile with PKI{}.Error: {}".format(profile_name, str(e))
        )

def configure_dot1x_pae(device, intf, mode='both'):

    """Configure
    dot1x pae {mode}

    Args:
        device (`obj`): Device object
        intf (`str`): Interface to configure
        mode ('str', optional): Mode to configure, defaults to 'both'

    Return:
        None

    Raise:
        SubCommandFailure: Failed configuring dot1x pae on interface
    """

    try:
        device.configure([
            f"interface {intf}",
            f"dot1x pae {mode}"
        ])

    except SubCommandFailure:
        log.error('Failed configuring dot1x pae command on interface')


def unconfigure_dot1x_pae(device, intf, mode='both'):

    """Unconfigure
    no dot1x pae {mode}

    Args:
        device (`obj`): Device object
        intf (`str`): Interface to configure
        mode ('str', optional): Mode to unconfigure, defaults to 'both'

    Return:
        None

    Raise:
        SubCommandFailure: Failed unconfiguring dot1x pae on interface
    """

    try:
        device.configure([
            f"interface {intf}",
            f"no dot1x pae {mode}"
        ])

    except SubCommandFailure:
        log.error('Failed configuring dot1x pae command on interface')


def configure_service_template_linksec(device, template, session_type):
    """Configure Service template with link security
        Args:
            device ('obj'): device to use
            template (`str`): template name
            session_type (`str`): session type to be configured

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure Service template with link security
    """

    cmd = [
        f'service-template {template}',
        f'linksec policy {session_type}',
    ]

    log.debug("Configure Service template with link security")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Service template with link security")


def unconfigure_service_template(device, template):
    """Unconfigure Service template
        Args:
            device ('obj'): device to use
            template (`str`): template name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to unconfigure Service template
    """
    cmd = f'no service-template {template}'

    log.debug("Unconfigure Service template")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Service template")


def configure_service_template_voice(device, template):
    """Configure Service template with voice
        Args:
            device ('obj'): device to use
            template (`str`): template name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure Service template with voice
    """

    cmd = [
        f'service-template {template}',
        'voice vlan'
          ]

    log.debug("Configure Service template with voice")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Service template with voice")


def configure_class_map_subscriber(device,
                                   map_name,
                                   match_type,
                                   result_type=None,
                                   auth_status=None,
                                   method_type=None,
                                   dot1x_type=None,
                                   priority_type=None,
                                   priority=None):
    """Configure Class Map Subscriber
        Args:
            device ('obj'): device to use
            map_name ('str'): map name
            match_type ('str'): Match type
            result_type ('str', optional): Result type, defaults to None
            auth_status ('str', optional): Authorization status, defaults to None
            method_type ('str', optional): Method type, defaults to None
            dot1x_type ('str', optional): Dot1x type, defaults to None
            priority_type('str', optional): Priority type, defaults to None
            priority ('str', optional): Priorit value, defaults to None

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure Class map Subscriber
    """
    log.debug("Configure Class map Subscriber")

    cmd = [f'class-map type control subscriber match-all {map_name}']
    if result_type and method_type and dot1x_type:
       cmd.append (f'match {match_type} {result_type} {method_type} {dot1x_type}')
    elif result_type:
       cmd.append (f'match {match_type} {result_type}')
    elif auth_status:
       cmd.append (f'match {match_type} {auth_status}')
    elif method_type:
       cmd.append (f'match {match_type} {method_type}')
    elif priority_type:
       cmd.append (f'match {match_type} {priority_type} {priority}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
         "Could not configure Class map Subscriber")
    return

def unconfigure_class_map_subscriber(device, map_name):
    """Unconfigure Class Map Subscriber
        Args:
            device ('obj'): device to use
            map_name (`str`): map name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to unconfigure Class Map Subscriber
    """
    cmd = f'no class-map type control subscriber match-all {map_name}'

    log.debug("Unconfigure Class Map Subscriber")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure Class Map Subscriber")


def configure_dot1x_cred_int(device, interface, cred_profile_name=None, eap_profile=None, auth_profile=None):
    """Configure Dot1x credential on interface
    Args:
        device ('obj'): device to use
        interface (`str`): Interface name
        cred_profile_name (`str', optional): dot1x credential profile name
        eap_profile (`str`, optional): eap profile name (Default is None)
        auth_profile (`str`, optional): Auth profile name(Default is None)

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to configure Dot1x credential on interface
    """
    converted_interface = Common.convert_intf_name(interface)
    cmd = []
    cmd.append(f'interface {converted_interface}')

    if cred_profile_name:
        cmd.append(f'dot1x credentials {cred_profile_name}')

    if eap_profile is not None:
        cmd.append(f'dot1x supplicant eap profile {eap_profile}')

    if auth_profile is not None:
       cmd.append(f'dot1x authenticator eap profile {auth_profile}')


    log.debug("Configure dot1x credential on interface")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure credential on interface on {}.Error: {}".format(converted_interface, str(e))
        )


def unconfigure_dot1x_cred_int(device, interface, cred_profile_name=None, eap_profile=None, auth_profile=None):
    """Unconfigure Dot1x credential on interface
    Args:
        device ('obj'): device to use
        interface (`str`): Interface name
        cred_profile_name (`str', optional): dot1x credential profile name (Default is None)
        eap_profile (`str`, optional): eap profile name (Default is None)
        auth_profile (`str`, optional): Auth profile name (Default is None)

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to unconfigure Dot1x credential on interface
    """
    converted_interface = Common.convert_intf_name(interface)
    cmd = []
    cmd.append(f'interface {converted_interface}')

    if cred_profile_name:
        cmd.append(f'no dot1x credentials {cred_profile_name}')

    if eap_profile is not None:
        cmd.append(f'no dot1x supplicant eap profile {eap_profile}')

    if auth_profile is not None:
       cmd.append(f'no dot1x authenticator eap profile {auth_profile}')


    log.debug("Unconfigure dot1x credential on interface")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure credential on interface on {}.Error: {}".format(converted_interface, str(e))
        )

def configure_radius_server_accounting_system(device,minutes,seconds,privilege_level,auth_list):
    """ configure radius-server accounting system host-config
    Args:
        device ('obj'): Device object
        minutes ('int): Specify timeout in minutes
        seconds ('int'): Specify timeout in seconds
        privilege_level ('int'): Specify privilege level for line
        auth_list ('str') : Specify authentication list
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring radius-server accounting system host-config
    """
    log.info(f"Configuring radius-server accounting system host-config")

    configs=[
        "radius-server accounting system host-config",
        "line console 0",
        f"exec-timeout {minutes} {seconds}",
        f"privilege level {privilege_level}",
        f"login authentication {auth_list}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure radius-server accounting system host-config. Error:\n{e}")

def configure_service_template_with_inactivity_timer(device,template_name,timer):
    """ configure service template with inactivity timer
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        timer ('int'): inactivity timer value
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring service template with inactivity timer
    """
    log.info(f"Configuring service template with inactivity timer")

    configs=[
	    f"service-template {template_name}",
	    f"inactivity-timer {timer}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with inactivity timer. Error:\n{e}")

def configure_service_template_with_vlan(device,template_name,vlan_id):
    """ configure service template with vlan
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        vlan_id ('int'): Vlan ID to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring service template with vlan
    """
    log.info(f"Configuring service template with vlan")

    configs=[
	    f"service-template {template_name}",
	    f"vlan {vlan_id}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with vlan. Error:\n{e}")

def configure_service_template_with_access_group(device,template_name,access_grp):
    """ configure service template with access group
    Args:
        device ('obj'): Device object
        template_name ('str): Specify a template name
        access_grp ('str'): Access-Group
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring service template with access group
    """
    log.info(f"Configuring service template with access group")

    configs=[
	    f"service-template {template_name}",
	    f"access-group {access_grp}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with access group. Error:\n{e}")

def configure_class_map_type_match_any(device,class_map_name,service_temp_name):
    """ configure class-map type control subscriber match-any
    Args:
        device ('obj'): Device object
        class_map_name ('str): Specify a class map name
        service_temp_name ('str'): Specify service template name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring class-map type control subscriber match-any
    """
    log.info(f"Configuring service template with access group")

    configs=[
	    f"class-map type control subscriber match-any {class_map_name}",
	    f"match activated-service-template {service_temp_name}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure class-map type control subscriber match-any. Error:\n{e}")

def configure_class_map_type_match_none(device,class_map_name,service_temp_name):
    """ configure class-map type control subscriber match-none
    Args:
        device ('obj'): Device object
        class_map_name ('str): Specify a class map name
        service_temp_name ('str'): Specify service template name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring class-map type control subscriber match-none
    """
    log.info(f"Configuring service template with access group")

    configs=[
	    f"class-map type control subscriber match-none {class_map_name}",
	    f"match activated-service-template {service_temp_name}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure class-map type control subscriber match-none. Error:\n{e}")

def configure_template_methods_for_dot1x(device,template_name,vlan_id,voice_vlan_id,policy_map_name):
    """ configure template methods for dot1x
    Args:
        device ('obj'): Device object
        template_name ('str): Specify template name
        vlan_id ('str'): Specify VLAN ID of the VLAN when this port is in access mode
        voice_vlan_id ('str'): Specify Vlan for voice traffic
        policy_map_name ('str'): Policy-map name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring template methods for dot1x
    """
    log.info(f"Configuring template methods for dot1x")

    configs=[
        f"template {template_name}",
        "dot1x pae authenticator",
        f"switchport access vlan {vlan_id}",
        "switchport mode access",
        f"switchport voice vlan {voice_vlan_id}",
        "mab",
        "access-session closed",
        "access-session port-control auto",
        "authentication periodic",
        "authentication timer reauthenticate server",
	    f"service-policy type control subscriber {policy_map_name}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure template methods for dot1x. Error:\n{e}")

def configure_template_methods_using_max_reauth(device,template_name,timeout_period,max_reauth):
    """ configure template methods using max reauth and timeout
    Args:
        device ('obj'): Device object
        template_name ('str): Specify template name
        timeout_period ('int'): Specify VLAN ID of the VLAN when this port is in access mode
        max_reauth ('int'): Specify max-reauth-req value <1-10>
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring template methods using max reauth and timeout
    """
    log.info(f"Configuring template methods for dot1x")

    configs=[
        f"template {template_name}",
        f"dot1x timeout tx-period {timeout_period}",
        f"dot1x max-reauth-req {max_reauth}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure template methods using max reauth and timeout. Error:\n{e}")

def clear_access_session_mac(device, mac):
    """Clear Access Session MAC
    Args:
        device ('obj'): device to use
        mac (`str`): MAC to be cleared

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to clear access session mac
    """
    log.debug("Clearing Access session MAC")
    try:
        device.execute(f'clear access-session mac {mac}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to clear Access session MAC.Error: {}".format(str(e))
        )

def unconfigure_source_template(device, interface, template_name):
    """Unconfigure Source template config
        Args:
            device ('obj'): device to use
            interface (`str`): Interface name
            template (`str`): Built-in/User defined template Name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to remove the source template
    """

    converted_interface = Common.convert_intf_name(interface)
    cmd = [
                f"interface {interface}",
                f"no source template {template_name}"
          ]
    log.info("Unconfigure source template {tmp} on {intf}".format(tmp=template_name, intf=converted_interface))

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure the source template {}.Error: {}".format(template_name, str(e))
        )


def configure_service_policy(device, policy_name):
    """Configure Service policy
        Args:
            device ('obj'): device to use
            policy_name (`str`): Policy_name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure Service policy
    """

    cmd = [f'service-policy type control subscriber {policy_name}']

    log.debug("Configure Service policy")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Service policy")


def unconfigure_service_policy(device):
    """Unconfigure Service policy
        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to unconfigure Service policy
    """

    cmd = ['no service-policy type control subscriber']

    log.debug("Unconfigure Service policy")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Service policy")


def configure_access_session_limit(device, session_limit, event_limit):
    """Configure Access session and event limit
        Args:
            device ('obj'): device to use
            session_limit (`int`): Session Limit or max sessions to be logged
            event_limit ('int'): Event Limit per session

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure Access session and event limit
    """

    cmd = [f'access-session event-logging enable session-limit {session_limit} event-limit {event_limit}']

    log.debug("Configure Access session and event limit")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Access session and event limit")


def unconfigure_access_session_limit(device):
    """Unconfigure Access session and event limit
        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to unconfigure Access session and event limit
    """

    cmd = ['no access-session event-logging enable session-limit']

    log.debug("Unconfigure Access session and event limit")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Access session and event limit")


def unconfigure_dot1x_template(device, template_name):
    """template unconfig
        Args:
            device ('obj'): device to use
            template (`str`): Built-in/User defined template Name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to unconfigure template
    """
    cmd = ''
    cmd += f'no template {template_name}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure template {}.Error: {}".format(template_name, str(e))
        )


def configure_parameter_map_subscriber(device, parameter_map_name, map_num,
    filter_type, parameter_type, parameter_name, action_num, template_type,
    template_name):
    """Configure parameter map subscriber
        Args:
            device ('obj'): device to use
            parameter_map_name (`str`): Parameter Map name to be configured
            map_num ('int'): Map number to be configured
            filter_type ('str'): Filter type to be configured
            parameter_type ('str'): parameter type to be configured
            parameter_name ('str'): Parameter name to be configured
            action_num ('int'): Action number to be configure
            template_type ('str'): Template type to be configured
            template_name ('str'): Template name to be configured

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure parameter map subscriber
    """
    cmd = ''
    cmd += f'parameter-map type subscriber attribute-to-service {parameter_map_name}\n'
    cmd = [  f'parameter-map type subscriber attribute-to-service {parameter_map_name}\n',
                   f'{map_num} map {parameter_type} {filter_type} {parameter_name}\n',
                   f'{action_num} {template_type} {template_name}' ]


    log.debug("Configure parameter map subscriber")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure parameter map subscriber")


def configure_service_template_with_absolute_timer(device, template_name, timer):
    """ configure service template with absolute timer
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        timer ('int'): timer
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with absolute timer")

    configs=[
	    f"service-template {template_name}",
	    f"absolute-timer {timer}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with absolute timer. Error:\n{e}")

def configure_service_template_with_description(device, template_name, desc_line):
    """ configure service template with description
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        desc_line ('str'): description line
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with description")

    configs=[
	    f"service-template {template_name}",
	    f"description {desc_line}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with description. Error:\n{e}")

def configure_service_template_with_inactivity_timer(device, template_name, timer, probe=None):
    """ configure service template with inactivity timer
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        timer ('int'): timer
        probe('str',optional): probe
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with inactivity timer")

    cmd = []
    cmd.append(f"service-template {template_name}")
    if probe:
        cmd.append(f"inactivity-timer {timer} probe")
    else:
        cmd.append(f"inactivity-timer {timer}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with inactivity timer. Error:\n{e}")

def configure_service_template_with_redirect_url(device, template_name, url_link, acl_name="", redirect_option=""):
    """ configure service template with redirect url
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        url_link ('str'): url link
        acl_name('str'): acl name
        redirect_option('str'): redirect option
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with redirect url")

    cmd = []
    cmd.append(f"service-template {template_name}")
    if acl_name:
        if redirect_option:
            cmd.append(f"redirect url {url_link} match {acl_name} {redirect_option}")
        else:
            cmd.append(f"redirect url {url_link} match {acl_name}")
    else:
        cmd.append(f"redirect url {url_link}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with redirect url. Error:\n{e}")

def configure_service_template_with_sgt(device, template_name, sgt_range):
    """ configure service template with sgt
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        sgt_range ('int'): sgt range
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with sgt")

    configs=[
	    f"service-template {template_name}",
	    f"sgt {sgt_range}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with sgt. Error:\n{e}")

def configure_service_template_with_tag(device, template_name, tag):
    """ configure service template with sgt range
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        tag ('str'): tag name
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with tag")

    configs=[
	    f"service-template {template_name}",
	    f"tag {tag}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with tag. Error:\n{e}")

def unconfigure_autoconf(device):
    """ Unconfigure autoconf enable

    Args:
        device ('obj'): device to use
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = 'no autoconf enable'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to  Unconfigure autoconf enable on this device. Error:\n{e}")

def configure_service_template_with_command_line(device, template_name, command):
    """ configure service template with command
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        command ('str'): command to configure
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with command")

    configs=[
	    f"service-template {template_name}",
	    f"{command}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with command. Error:\n{e}")

def configure_authentication_control_direction(device, interface, direction):

    """Configure authentication control-direction
    Args:
        device ('obj'): Device object
        interface ('str'): Interface to configure
        direction ('str'): Control traffic direction (both/in)
    Return:
        None
    Raise:
        SubCommandFailure
    """

    cmd = [
        f'interface {interface}',
        f'authentication control-direction {direction}'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure authentication control-direction. Error:\n{e}")

def unconfigure_authentication_control_direction(device, interface, direction):

    """Unconfigure authentication control-direction
    Args:
        device ('obj'): Device object
        interface ('str'): Interface to configure
        direction ('str'): Control traffic direction (both/in)
    Return:
        None
    Raise:
        SubCommandFailure
    """

    cmd = [
        f'interface {interface}',
        f'no authentication control-direction {direction}'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure authentication control-direction. Error:\n{e}")

def configure_authentication_open(device, interface):

    """Configure authentication open
    Args:
        device ('obj'): Device object
        interface ('str'): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure
    """

    cmd = [
        f'interface {interface}',
        'authentication open'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure authentication open. Error:\n{e}")

def unconfigure_authentication_open(device, interface):

    """Unconfigure authentication open
    Args:
        device ('obj'): Device object
        interface ('str'): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure
    """

    cmd = [
        f'interface {interface}',
        'no authentication open'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure authentication open. Error:\n{e}")
