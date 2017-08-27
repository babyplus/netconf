import os
import sys
import platform
import re
import time
sys.path.append('/var/jenkins_home/project/ansible/huang_h3c_netconf/huang_h3c_netconf')
from lib.NetconfMission import XmlMission
from lib.NetconfMission import CommandMission
from conf import HostsConf


path = HostsConf.path
xml_file = HostsConf.xml_file


def wait_host():
    print("rebooting switch ...")
    if platform.system() == 'Windows':
        test_ping = 'ping {}'
    elif platform.system() == 'Linux':
        test_ping = 'ping {} -c4'
    else:
        print('not support')
        exit(1)
    for machine in HostsConf.init:
        time.sleep(180)
        for n in range(21):
            time.sleep(60)
            try:
                ret = os.system(test_ping.format(HostsConf.init[machine]['ip']))
            except Exception:
                pass
            if ret == 0:
                break
            if n == 20:
                print('timeout...')
                exit(1)

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
    XmlMission(path, HostsConf.init).run()
    CommandMission(path, HostsConf.init).run("get_all_config", super_module='VLAN', sub_module='TrunkInterfaces')