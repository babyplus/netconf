import os
import sys
import platform
import re
import time
from xml.etree import ElementTree as ET
sys.path.append('/var/jenkins_home/project/ansible/huang_h3c_netconf/huang_h3c_netconf')
from lib.NetconfMission import XmlMission
from lib.NetconfMission import CommandMission
from conf import HostsConf


path = HostsConf.path
xml_file = HostsConf.xml_file


def wait_host():
    print("rebooting switch ...")
    time.sleep(720)

def check_irf_config():
    print("rebooting switch ...")
    time.sleep(180)
    for n in range(21):
        time.sleep(60)
        try:
            if n == 20:
                print('connect timeout .')
                exit(1)
            b = CommandMission(path, HostsConf.init).run("get_config", super_module='IRF', sub_module='IRFPorts')
            if len(re.findall(r'<MemberID>', b)) > 1:
                print("irf_config ok...")
                break
        except Exception :
            pass

def process():
    # rename irf_member2 number ,reboot it
    try:
        CommandMission(path, HostsConf.irf_init).run("sys_CLI")
    except Exception as e:
        pass
    time.sleep(5)
    try:
        CommandMission(path, HostsConf.irf_init).run("user_CLI")
    except Exception as e:
        pass
    ######################################
    # check machine running
    wait_host()
    #######################

    # config irf configuration
    XmlMission(path, HostsConf.irf_init).run()
    CommandMission(path, HostsConf.irf_init).run("save", FileName='startup.cfg', FileOverWrite='true' )
    try:
        CommandMission(path, HostsConf.irf_init).run("sys_CLI", sys_cli_command='irf-port-configuration active')
    except Exception as e:
        pass
    ##########################

    # check machine running
    check_irf_config()
    #######################

    # others
    XmlMission(path, HostsConf.init).run()
    CommandMission(path, HostsConf.init).run("save", FileOverWrite='true', FileName='test.cfg')
    #########

if __name__ == '__main__':
    #XmlMission(path, HostsConf.init).run()
    hosts_conf = '''

    {"0": {
            "ip": "10.218.2.232", "password": "gsta123",
           "xml_file": {
                        "0": "xml_files/openstack/LAGG_interfaces_conf.xml"
                        }, "user": "admin", "oem": "h3c"
            }
    }

    '''
    import json
    ret = json.loads(hosts_conf)