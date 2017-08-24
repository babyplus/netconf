import os
import sys
import platform
import re
import time
sys.path.append('/root/net_test/huang_h3c_netconf')
from lib.NetconfMission import XmlMission
from lib.NetconfMission import CommandMission
from conf import HostsConf


path = HostsConf.path
xml_file = HostsConf.xml_file


def wait_host():
    if platform.system() == 'Windows':
        test_ping = 'ping {}'
    elif platform.system() == 'Linux':
        test_ping = 'ping {} -c4'
    else:
        print('not support')
        exit(1)
    for host_ip in HostsConf.irf_init:
        time.sleep(180)
        for n in range(21):
            ret = os.system(test_ping.format(HostsConf.irf_init[host_ip]['ip']))
            if ret == 0:
                break
            if n == 20:
                print('timeout...')

def check_irf_config():
    print("rebooting switch ...")
    time.sleep(180)
    for n in range(21):
        time.sleep(60)
        try:
            if n == 20:
                print('connect timeout .')
                exit(1)
            a = CommandMission(path, HostsConf.init).run("get_config", super_module='IRF', sub_module='IRFPorts')
            if len(re.findall(r'<MemberID>', a)) > 1:
                break
        except Exception :
            pass

if __name__ == '__main__':
    # rename irf_member2 number ,reboot it
    '''
    try:
        CommandMission(path, HostsConf.irf_init).run("sys_CLI")
    except Exception as e:
        pass
    '''
    ######################################
    # check machine running
    '''no implement'''
    #wait_host()
    #######################

    # config irf configuration
    '''
    XmlMission(path, HostsConf.irf_init).run()
    CommandMission(path, HostsConf.irf_init).run("save", FileName='startup.cfg', OverWrite='true' )
    try:
        CommandMission(path, HostsConf.irf_init).run("sys_CLI", sys_cli_command='irf-port-configuration active')
    except Exception as e:
        pass
    '''
    ##########################

    # check machine running
    '''no implement'''
    #check_irf_config()

    #######################

    # others
    #XmlMission(path, HostsConf.init).run()
    CommandMission(path, HostsConf.init).run("save", OverWrite='true', FileName='test.cfg')
    #########
