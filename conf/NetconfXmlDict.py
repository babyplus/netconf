import os

'''
test connect without do anything: <default-operation>none</default-operation>
meet error :<error-option>continue-on-error/ stop-on-error/ rollback-on-error</error-option>

'''
tmp = '''
<rpc message-id ="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<edit-config>
<target>
<running/>
</target>
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
<top xmlns="http://www.{oem}.com/netconf/config:1.0">
{%s}
</top>
</config>
</edit-config>
</rpc>
'''

dict = {
    'get_config': {
        'h3c_xml': '''
        <rpc message-id ="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:xc="http://www.{oem}.com/netconf/base:1.0">
        <get-config>
        <source>
        <running/>
        </source>
        <filter type="subtree">
        <top xmlns="http://www.{oem}.com/netconf/config:1.0">
        <{super_module}>
        <{sub_module}>
        </{sub_module}>
        </{super_module}>
        </top>
        </filter>
        </get-config>
        </rpc>
        '''
    },

    'get_all_config': {
        'h3c_xml': '''
        <rpc message-id ="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:xc="http://www.{oem}.com/netconf/base:1.0">
        <get-config>
        <source>
        <running/>
        </source>
        <filter type="subtree">
        <top xmlns="http://www.{oem}.com/netconf/config:1.0">
        </top>
        </filter>
        </get-config>
        </rpc>
        '''
    },

    'get_all': {
        'h3c_xml': ''''
        <rpc message-id ="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:xc="http://www.{oem}.com/netconf/base:1.0">
        <get>
        <filter type="subtree">
        <top xmlns="http://www.{oem}.com/netconf/data:1.0">
        </top>
        </filter>
        </get>
        </rpc>
        '''
    },

    'get_module': {
        'h3c_xml': '''
        <rpc message-id ="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:xc="http://www.{oem}.com/netconf/base:1.0">
        <get>
        <filter type="subtree">
        <top xmlns="http://www.{oem}.com/netconf/data:1.0">
        <{super_module}>
        <{sub_module}>
        </{sub_module}>
        </{super_module}>
        </top>
        </filter>
        </get>
        </rpc>
        '''
    },

    'clear': {
        'h3c_xml': '''
        <rpc message-id="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <action>
        <top xmlns="http://www.{oem}.com/netconf/action:1.0">
        <Ifmgr>
        <ClearAllIfStatistics>
        <Clear>
        </Clear>
        </ClearAllIfStatistics>
        </Ifmgr>
        </top>
        </action>
        </rpc>
        '''
    },

    'shutdown': {
        'Description': '1 power on ; 2 power off',
        'h3c_xml': '''
        <rpc message-id ="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <edit-config>
        <target>
        <running/>
        </target>
        <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <top xmlns="http://www.{oem}.com/netconf/config:1.0">
        <Ifmgr>
        <Interfaces>
        <Interface>
        <IfIndex>{IfIndex}</IfIndex>
        <AdminStatus>{AdminStatus}</AdminStatus>
        </Interface>
        </Interfaces>
        </Ifmgr>
        </top>
        </config>
        </edit-config>
        </rpc>
    '''
    },

    'sys_CLI': {
        'h3c_xml': '''
        <rpc message-id="100"
        xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <CLI>
        <Configuration>{sys_cli_command}</Configuration>
        </CLI>
        </rpc>
        '''
    },

    'user_CLI': {
        'h3c_xml': '''
        <rpc message-id="100"
        xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <CLI>
        <Execution>{user_cli_command}</Execution>
        </CLI>
        </rpc>
        '''
    },

    'save': {
        'h3c_xml': '''
        <rpc message-id="100"
        xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <save OverWrite="{OverWrite}">
        <file>{FileName}</file>
        </save>
        </rpc>
        '''
    },

    'interface': {
        'h3c_xml': '''
        <rpc message-id ="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <edit-config>
        <target>
        <running/>
        </target>
        <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <top xmlns="http://www.{oem}.com/netconf/config:1.0">
        <Ifmgr>
        <Interfaces>
        <Interface>
        <IfIndex>{IfIndex}</IfIndex>
        <LinkType>{LinkType}</LinkType>
        <PVID>{PVID}</PVID>
        </Interface>
        </Interfaces>
        </Ifmgr>
        </top>
        </config>
        </edit-config>
        </rpc>
        '''
    },

    'interfaces': {
        'h3c_xml': '''
        <rpc message-id ="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <edit-config>
        <target>
        <running/>
        </target>
        <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <top xmlns="http://www.{oem}.com/netconf/config:1.0">
        <Ifmgr>
        {Interfaces_conf}
        </Ifmgr>
        </top>
        </config>
        </edit-config>
        </rpc>
        '''
    },

    'IRF': {
        'h3c_xml': '''
        <rpc message-id ="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <edit-config>
        <target>
        <running/>
        </target>
        <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <top xmlns="http://www.{oem}.com/netconf/config:1.0">
        {IRF_conf}
        </top>
        </config>
        </edit-config>
        </rpc>
        '''
    },
    'LAGG': {
        'h3c_xml': '''
        <rpc message-id ="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <edit-config>
        <target>
        <running/>
        </target>
        <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <top xmlns="http://www.{oem}.com/netconf/config:1.0">
        {LAGG_conf}
        </top>
        </config>
        </edit-config>
        </rpc>
    '''
    },

}
