import json
def get(**kwargs):
    a = json.dumps(kwargs)
    return a

ret = get(super_module='IRF', sub_module='IRFPorts',sys_cli_command='irf-port-configuration active',FileName='startup.cfg', FileOverWrite='true')

print(ret)