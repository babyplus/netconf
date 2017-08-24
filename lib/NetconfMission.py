import copy
from lib.NetConfObject import NetConfRun

class Mission(object):
    def __init__(self, path, hosts_conf, **kwargs):
        self.path = path
        self.hosts_conf = hosts_conf
        self.mission_kwargs = kwargs

    def uniq_key(self, new_dict, old_dict):
        for n in new_dict.keys():
            try:
                old_dict.pop(n)
            except Exception as e:
                pass


class CommandMission(Mission):
    def run(self, mission, **kwargs):
        tmp_kwargs = copy.deepcopy(kwargs)
        for n in self.hosts_conf.keys():
            init = self.hosts_conf[n]
            init['path'] = self.path
            init['xml_file'] = mission
            self.uniq_key(tmp_kwargs, init)
            kwargs.update(init)
            print('{ip} >>> begin'.format(**kwargs))
            print("mission: {}".format(mission))
            ret = NetConfRun(**kwargs).run_mission('{}'.format(mission), **kwargs)
            print('{ip} >>> end'.format(**kwargs))
        return ret


class XmlMission(Mission):
    def run(self, **kwargs):
        tmp_kwargs = copy.deepcopy(kwargs)
        for n in self.hosts_conf.keys():
            init = self.hosts_conf[n]
            init['path'] = self.path
            if not 'xml_file' in init:
                init['xml_file'] = self.mission_kwargs.get('xml_file')
            self.uniq_key(tmp_kwargs, init)
            kwargs.update(init)
            init_tmp = kwargs['xml_file']
            print('{ip} >>> begin'.format(**kwargs))
            print("missions : {}".format(init['xml_file']))
            for m in range(len(init_tmp)):
                init['xml_file'] = init_tmp[m]
                print("init>>")
                NetConfRun(**init).run_xml_conf("{path}/{xml_file}".format(**init))
            print('{ip} >>> end'.format(**kwargs))
