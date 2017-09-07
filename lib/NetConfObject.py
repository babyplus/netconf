import logging as LOG
import re
from conf import NetconfXmlDict
from lib import netconf
from lib.DataCollect import DebugCollect


class NetConfRun(object):
    def __init__(self, **kwargs):
        self.init = kwargs
        self.netconf_client = netconf.NETCONF(**self.init)

    def run_mission(self, mission, **kwargs):
        kwargs.update(self.init)
        if self.netconf_client is not None:
            if NetconfXmlDict.dict.get("{}".format(mission)) is None:
                LOG.error("need to add '{}' mission in netconf_xml_dict file".format(mission))
                exit(1)
            try:
                resp = self.netconf_client.run(
                    NetconfXmlDict.dict.get(mission).get('{oem}_xml'.format(**self.init)).format(**kwargs),
                    **self.init
                )
                DebugCollect('result.xml', resp, **kwargs)
            except TypeError:
                if mission == "user_CLI":
                    pass
            except Exception as e:
                print kwargs
                LOG.error("need to set {} value as argument or maybe use a illegal keyword in NetconfXmlDict".format(e))
                exit(2)
        return resp

    def run_xml_conf(self, mission_file):
        dict_mission = {}
        file_name = re.search(r'[^\\/:*?"<>|\r\n]+$', mission_file).group()
        mission_name = re.search(r'.*[^.xml]', file_name).group()
        print("mission :" + mission_name)
        with open('{}'.format(mission_file), 'rb') as f:
            content = f.read()
            dict_mission['{}'.format(mission_name)] = content
            NetconfXmlDict.dict['{}'.format(mission_name)] = {
                '{oem}_xml'.format(**self.init): '''{}'''.format(NetconfXmlDict.tmp % mission_name)
            }
        self.run_mission('{}'.format(mission_name), **dict_mission)