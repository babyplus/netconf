path="/var/jenkins_home/project/ansible/huang_h3c_netconf/huang_h3c_netconf"
. ${path}/examples/jenkins/functions.sh

hosts_irf_conf='
{"0": {"user_cli_command": "dis th",
           "ip": "10.218.2.232",
           "sys_cli_command": "dis th",
           "user": "admin",
           "oem": "h3c",
           "password": "gsta123"},
     "1": {"user_cli_command": "reboot",
           "ip": "10.218.2.233",
           "sys_cli_command": "irf member 1 renumber 2",
           "user": "admin",
           "oem": "h3c",
           "password": "gsta123"}}
'
command_mission "$hosts_irf_conf" "sys_CLI"

hosts_irf_conf='
{"0": {"user_cli_command": "dis th",
           "ip": "10.218.2.232",
           "sys_cli_command": "dis th",
           "user": "admin",
           "oem": "h3c",
           "password": "gsta123"},
     "1": {"user_cli_command": "reboot",
           "ip": "10.218.2.233",
           "sys_cli_command": "irf member 1 renumber 2",
           "user": "admin",
           "oem": "h3c",
           "password": "gsta123"}}
'
command_mission "$hosts_irf_conf" "user_CLI"

echo wait for rebooting...
sleep 480

hosts_irf_conf='
{"0": {"xml_file": {"0": "xml_files/irf/interface41-48_shutdown.xml",
                        "1": "xml_files/irf/IRF_member1.xml",
                        "2": "xml_files/irf/interface41-48_no_shutdown.xml"},
           "ip": "10.218.2.232",
           "user": "admin",
           "oem": "h3c",
           "password": "gsta123"},
     "1": {"xml_file": {"0": "xml_files/irf/interface41-48_shutdown_member2.xml",
                        "1": "xml_files/irf/IRF_member2.xml",
                        "2": "xml_files/irf/interface41-48_no_shutdown_member2.xml"},
           "ip": "10.218.2.233",
           "user": "admin",
           "oem": "h3c",
           "password": "gsta123"}}
'
single_mission "$hosts_irf_conf"

hosts_irf_conf='
{"0": {    "ip": "10.218.2.232",
           "user": "admin",
           "oem": "h3c",
           "password": "gsta123"},
     "1": {"ip": "10.218.2.233",
           "user": "admin",
           "oem": "h3c",
           "password": "gsta123"}}
'
value_set='
{"FileOverWrite": "true", "FileName": "startup.cfg"}
'
command_mission "$hosts_irf_conf" "save" "$value_set"

hosts_irf_conf='
{"0": {    "ip": "10.218.2.232",
           "user": "admin",
           "oem": "h3c",
           "password": "gsta123"},
     "1": {"ip": "10.218.2.233",
           "user": "admin",
           "oem": "h3c",
           "password": "gsta123"}}
'
value_set='
{"sys_cli_command": "irf-port-configuration active"}
'
command_mission "$hosts_irf_conf" "sys_CLI" "$value_set"

hosts_conf='
{"0": {"ip": "10.218.2.232", "password": "gsta123", "user": "admin", "oem": "h3c"}}
'
check_irf_config "$hosts_conf"

hosts_conf='
{"0": {"ip": "10.218.2.232", "password": "gsta123",
           "xml_file": {"0": "xml_files/openstack/VLAN_conf.xml", "1": "xml_files/openstack/interfaces_conf.xml",
                        "2": "xml_files/openstack/VLAN_PORT_conf.xml", "3":"xml_files/openstack/LAGG_conf.xml"}, "user": "admin", "oem": "h3c"}}
'
single_mission "$hosts_conf"

hosts_conf='
{"0": {"ip": "10.218.2.232", "password": "gsta123", "user": "admin", "oem": "h3c"}}
'
make_irf_interfaces_conf "$hosts_conf"

hosts_conf='
    {"0": {
            "ip": "10.218.2.232", "password": "gsta123",
           "xml_file": {
                        "0": "xml_files/openstack/LAGG_interfaces_conf.xml","1":"xml_files/openstack/LAGG_VlAN_conf.xml"
                        }, "user": "admin", "oem": "h3c"
            }
    }
'
single_mission "$hosts_conf"

