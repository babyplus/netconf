path = 'C:/Users/root/PycharmProjects/huang_h3c_netconf'

xml_file = {
    0:'xml_files/interfaces_conf.xml',
}

init = {
    0:{
        'oem':'h3c',
        'ip':'10.218.2.232',
        'user':'admin',
        'password':'123456',
        'xml_file':{
            0: 'xml_files/openstack/VLAN_conf.xml',
            1: 'xml_files/openstack/interfaces_conf.xml',
            2: 'xml_files/openstack/LAGG_conf.xml',
            3: 'xml_files/openstack/IRF_interfaces_conf.xml',
            4: 'xml_files/openstack/VLAN_PORT_conf.xml',
        },
    },
}

irf_init = {
    0:{
        'oem':'h3c',
        'ip':'10.218.2.232',
        'user':'admin',
        'password':'123456',
        'xml_file':{
            0: 'xml_files/irf/interface41-48_shutdown.xml',
            1: 'xml_files/irf/IRF_member1.xml',
            2: 'xml_files/irf/interface41-48_no_shutdown.xml',
        },
        'sys_cli_command': 'dis th',
        'user_cli_command': 'dis th'
    },
    1: {
        'oem': 'h3c',
        'ip': '10.218.2.233',
        'user': 'admin',
        'password': '123456',
        'xml_file': {
            0: 'xml_files/irf/interface41-48_shutdown_member2.xml',
            1: 'xml_files/irf/IRF_member2.xml',
            2: 'xml_files/irf/interface41-48_no_shutdown_member2.xml',
        },
        'sys_cli_command': 'irf member 1 renumber 2',
        'user_cli_command': 'reboot'
    },
}