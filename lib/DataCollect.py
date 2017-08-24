import os
import datetime
import re
class DataCollect:
    def __init__(self,file_name, content, **kwargs):
        self.collect(file_name, content, **kwargs)

    def collect(self, file_name, content, **kwargs):
        file_name = re.search(r'[^\\/:*?"<>|\r\n]+$', kwargs.get('xml_file')).group().split(".")[0]
        kwargs['file_name'] = file_name
        return '{path}/%s/{ip}/{file_name}'.format(**kwargs) % DataCollect.class_name_str(self)

    def class_name_str(self):
        return str(self.__class__).split('.')[-1]


class DebugCollect(DataCollect):
    def collect(self, file_name, content, mark = None, **kwargs):
        debug_path = DataCollect.collect(self, file_name, content, **kwargs)
        if not os.path.exists(debug_path):
            os.makedirs(debug_path)
        with open(r"{}/{}{}".format(debug_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S_'), file_name), "wb") as r:
            r.write(content)
