# netconf
根据github上另外一个h3c netconf 的部分文件进行后续修改,用于批量化配置交换机。（需要先开启netconf的https调用功能，用soapui检测是否能正常使用）

conf文件夹主要放置配置文件，其中NetconfXmlDict.py文件可以对执行任务进行拓展，以供lib/NetconfMission/CommandMission 方法使用；
HostsConf.py文件为主机配置文件，将任务列表填在xml_file中后可以使用lib/NetconfMission/XmlMission 方法进行顺序执行；另外在个别主机中可以填写lib/NetconfMission/CommandMission 所需要的个别参数以达到多个主机不同命令的效果

lib文件夹主要放置比较核心的文件用于调用

xml_files存放了一些netconf的配置
