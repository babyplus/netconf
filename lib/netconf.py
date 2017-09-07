# -*- coding:utf-8 -*-

import urllib2
import httplib
from string import Template
from xml.etree import ElementTree as ET
import ssl
from lib.DataCollect import DebugCollect
#from lib import ssl

MESSAGE_ID = "100"
LANGUAGE_CH = "zh-cn"
LANGUAGE_EN = "en"

NS_HELLO = "{http://www.%s.com/netconf/base:1.0}"
NS_DATA = "{http://www.%s.com/netconf/data:1.0}"
HELLO = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
   <env:Header>
      <auth:Authentication env:mustUnderstand="1" xmlns:auth="http://www.%s.com/netconf/base:1.0">
         <auth:UserName>%s</auth:UserName>
         <auth:Password>%s</auth:Password>
      </auth:Authentication>
   </env:Header>
   <env:Body>
      <hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
         <capabilities>
            <capability>urn:ietf:params:netconf:base:1.0</capability>
         </capabilities>
      </hello>
   </env:Body>
</env:Envelope>"""

CLOSE = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
   <env:Header>
      <auth:Authentication env:mustUnderstand="1" xmlns:auth="http://www.$OEM.com/netconf/base:1.0">
         <auth:AuthInfo>$AuthInfo</auth:AuthInfo>
         <auth:Language>$Language</auth:Language>
      </auth:Authentication>
   </env:Header>
   <env:Body>
     <rpc message-id="$messageid"
          xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
       <close-session/>
     </rpc>
   </env:Body>
</env:Envelope>"""

RAW_TMP = '''
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
  <env:Header>
    <auth:Authentication env:mustUnderstand="1" xmlns:auth="http://www.$OEM.com/netconf/base:1.0">
      <auth:AuthInfo>$AuthInfo</auth:AuthInfo>
      <auth:Language>$Language</auth:Language>
    </auth:Authentication>
  </env:Header>
  <env:Body>
  {}
  </env:Body>
</env:Envelope>
'''

SESSION = """
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
   <env:Header>
      <auth:Authentication env:mustUnderstand="1" 
      xmlns:auth="http://www.$OEM.com/netconf/base:1.0">
         <auth:AuthInfo>$AuthInfo</auth:AuthInfo>
         <auth:Language>$Language</auth:Language>
      </auth:Authentication>
   </env:Header>
   <env:Body>
      <rpc message-id="$messageid" 
      xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
       <get-sessions/>
      </rpc>
   </env:Body>
</env:Envelope>"""


class NETCONF(object):
    def __init__(self, **kwargs):
        url = 'https://%s:832/soap/netconf/' % kwargs.get('ip')
        self.url = url
        self.oem = kwargs.get('oem')
        self.messageid = MESSAGE_ID
        self.Language = LANGUAGE_EN
        self.ns_data = NS_DATA % self.oem
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.AuthInfo = None

    def close_session(self):
        if self.AuthInfo is not None:
            close_template = Template(CLOSE)
            close_msg = close_template.substitute(OEM=self.oem,
                                                  AuthInfo=self.AuthInfo,
                                                  Language=self.Language,
                                                  messageid=self.messageid)
            try:
                req = urllib2.Request(self.url, close_msg)
                resp = urllib2.urlopen(req)
                self.AuthInfo = None
            except urllib2.URLError, err:
                print("Close session failed: %s", err)

    def request(self, req_msg, **kwargs):
        msg = Template(req_msg)
        MSG = msg.substitute(OEM=self.oem, Language=self.Language,
                             messageid=self.messageid,
                             AuthInfo=self.AuthInfo)
        DebugCollect('netconf.xml', MSG, **kwargs)
        req = urllib2.Request(self.url, MSG)
        if req is not None:
            try:
                ssl._create_default_https_context = ssl._create_unverified_context
                #context = ssl._create_unverified_context()
                resp = urllib2.urlopen(req, timeout=240)
                if resp is not None:
                    buf = resp.read()
                    return buf
                else:
                    print('Failed to open url %s', self.url)
            except Exception as e:
                print("Request failed %s, url %s", e, self.url)

    def get_session(self):
        if self.AuthInfo is not None:
            verify_msg = self.request(SESSION)
            root = ET.fromstring(verify_msg)
            is_return = True
            for element in root.iter("faultstring"):
                if element.text == 'Invalid session':
                    is_return = False
                    break
            if is_return is True:
                return

        hello_msg = HELLO % (self.oem, self.user, self.password)
        req_hello = urllib2.Request(self.url, hello_msg)
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            resp_hello = urllib2.urlopen(req_hello, timeout=120)
        except urllib2.URLError, err:
            if hasattr(err, "reason"):
                print('Failed to connect %s, Err:%s', self.url, err.reason)
            elif hasattr(err, "code"):
                print('Request failed, Err:%s', err.code)
            return
        except httplib.HTTPException as e:
            print("get session with HTTPException %s", e)
            return

        buf_hello = resp_hello.read()
        root = ET.fromstring(buf_hello)
        ns = NS_HELLO % self.oem
        for auth in root.iter(ns + "AuthInfo"):
            self.AuthInfo = auth.text
            break

    def run(self, raw, **kwargs):
        self.get_session()
        raw_msg_tmp = RAW_TMP.format(raw)
        return self.request(raw_msg_tmp, **kwargs)

