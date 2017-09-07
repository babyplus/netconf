import json
import sys
import time
import re
import os
import platform
sys.path.append('/var/jenkins_home/project/ansible/huang_h3c_netconf/huang_h3c_netconf')
from lib.NetconfMission import XmlMission
from lib.NetconfMission import CommandMission as RunCommand


def json_loads(raw):
    if raw is not None:
        try:
            ret = json.loads(raw)
        except ValueError:
            print("error: check the json format")
            exit(1)
        except Exception:
            pass
        return ret
    pass


def xml_mission_hosts_count(hosts_conf):
    a = json_loads(hosts_conf)
    print(len(a))
    return len(a)


def xml_mission_xml_count(hosts_conf, host_key):
    a = json_loads(hosts_conf)
    if a.has_key("{}".format(str(int(host_key)-1))):
        b = a["{}".format(str(int(host_key)-1))]["xml_file"]
    else:
        print("error hosts_conf, no exist key")
        b = ""
    print(len(b))
    return len(b)


def SingleXmlMission(hosts_conf, host_key, xml_key, path):
    a = json_loads(hosts_conf)
    tmp = a["{}".format(str(int(host_key)-1))]['xml_file'][str(int(xml_key)-1)]
    a["{}".format(str(int(host_key) - 1))]['xml_file'] = {}
    a["{}".format(str(int(host_key) - 1))]['xml_file']["0"] = tmp
    XmlMission("{}".format(path), a).run()


def CommandMission(hosts_conf, mission, path, *args):
    print(args)
    a = json_loads(hosts_conf)
    try:
        value = json_loads(args[0])
        print("arguments: {} ".format(value))
    except:
        value = {}
        print("use the default arguments in configuration")
    try:
        result = RunCommand(path, a).run(mission, **value)
    except Exception:
        pass
    return result

def json_test(value_set):
    a = json_loads(value_set)
    print(a)



def check_irf_config(hosts_conf, path):
    print("rebooting switch ...")
    a = json_loads(hosts_conf)
    time.sleep(180)
    for n in range(21):
        time.sleep(60)
        try:
            if n == 20:
                print('connect timeout .')
                exit(1)
            b = RunCommand(path, a).run("get_config", super_module='IRF', sub_module='IRFPorts')
            if len(re.findall(r'<MemberID>', b)) > 1:
                print("irf_config ok...")
                break
        except Exception :
            pass



def wait_host(hosts_conf, *args):
    a = json.loads(hosts_conf)
    print("rebooting switch ...")
    if platform.system() == 'Windows':
        test_ping = 'ping {}'
    elif platform.system() == 'Linux':
        test_ping = 'ping {} -c4'
    else:
        print('not support')
        exit(1)
    time.sleep(180)
    for machine in a:
        for n in range(21):
            time.sleep(60)
            try:
                ret = os.system(test_ping.format(a[machine]['ip']))
            except Exception:
                pass
            if ret == 0:
                print("ok")
                break
            if n == 20:
                print('timeout...')
                exit(1)

def pause(*args):
    time.sleep(30)

def get_bridgeAggregation_map(raw):
    bridgeAggregation_map = re.findall("<IfIndex>....</IfIndex><Name>Bridge-Aggregation.*</Name>", raw)
    bridgeAggregation_map = bridgeAggregation_map[0].replace("</IfIndex><Name>",":")\
        .replace("</Name></Interface><Interface>",":") \
        .replace("<IfIndex>", "") \
        .replace("</Name>","")
    return bridgeAggregation_map

def create_xml_for_LAGG(ifIndex, linkType, pVID=1, *args):
    text = '''
        <Interface>
            <IfIndex>{ifIndex}</IfIndex>
            <PVID>{pVID}</PVID>
            <LinkType>{linkType}</LinkType>
        </Interface>
    '''
    return text.format(ifIndex=ifIndex, pVID=pVID, linkType=linkType)

def create_xml_for_LAGG_VLAN(ifIndex, PermitVlanList="1", *args):
    text = '''
        <Interface>
            <IfIndex>{ifIndex}</IfIndex>
            <PermitVlanList>{PermitVlanList}</PermitVlanList>
        </Interface>
    '''
    return text.format(ifIndex=ifIndex, PermitVlanList=PermitVlanList)


def make_irf_interfaces_conf(hosts_conf, path, **kwargs):
    kwargs = {
        "LAGG_interfaces_conf_path":"xml_files/openstack/LAGG_interfaces_conf.xml",
        "LAGG_VLAN_conf_path": "xml_files/openstack/LAGG_VlAN_conf.xml",
        "interfaces":{
            "100-111":{
                "linkType":"1",
                "pVID": "1"
            },
            "200-211":{
                "linkType": "2",
                "pVID":"150",
                "PermitVlanList":"1,150-154"
            },
            "300-311":{
                "linkType": "1",
                "pVID": "1"
            }
        }
    }
    mission = "make_irf_interfaces_conf"
    raw = CommandMission(hosts_conf, mission, path)
    raw = get_bridgeAggregation_map(raw)
    raw_list = raw.split(":")
    raw_dict = {raw_list[2 * n + 1]:raw_list[2 * n] for n in range(len(raw_list)/2)}
    ifmgr_head_tail = '''
    <Ifmgr>
    <Interfaces>
    {}
    </Interfaces>
    </Ifmgr>
    '''
    vlan_head_tail = '''
    <VLAN>
    <TrunkInterfaces>
    {}
    </TrunkInterfaces>
    </VLAN>
        '''
    ifmgr_text_tmp = ""
    vlan_text_tmp = ""
    for i in kwargs["interfaces"].keys():
        for n in range(int(i.split("-")[0]), int(i.split("-")[1])+1):
            ifmgr_text_tmp = ifmgr_text_tmp + create_xml_for_LAGG(raw_dict["Bridge-Aggregation{}".format(str(n))],
                                                      kwargs["interfaces"]["{}".format(i)]["linkType"],
                                                      kwargs["interfaces"]["{}".format(i)]["pVID"]
                                                      )
            if kwargs["interfaces"]["{}".format(i)]["linkType"] == "2":
                vlan_text_tmp = vlan_text_tmp + create_xml_for_LAGG_VLAN(raw_dict["Bridge-Aggregation{}".format(str(n))],
                                                                         kwargs["interfaces"]["{}".format(i)]["PermitVlanList"]
                                                                         )
    with open("{path}/{LAGG_interfaces_conf_path}".
                      format(path=path,LAGG_interfaces_conf_path=kwargs["LAGG_interfaces_conf_path"]), "wb") as f:
        f.write(ifmgr_head_tail.format(ifmgr_text_tmp))
    with open("{path}/{LAGG_VLAN_conf_path}".
                      format(path=path,LAGG_VLAN_conf_path=kwargs["LAGG_VLAN_conf_path"]), "wb") as f:
        f.write(vlan_head_tail.format(vlan_text_tmp))



if __name__ == '__main__':
    eval(sys.argv[1])(*sys.argv[2:])