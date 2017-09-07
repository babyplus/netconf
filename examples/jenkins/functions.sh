single_mission()
{
for n in `seq $(python ${path}/examples/jenkins/test_json.py xml_mission_hosts_count "$1")`;do
  for m in `seq $(python ${path}/examples/jenkins/test_json.py xml_mission_xml_count "$1" "$n")`;do
    python ${path}/examples/jenkins/test_json.py SingleXmlMission "$1" "$n" "$m" "$path"
  done
done
}


command_mission()
{
  python ${path}/examples/jenkins/test_json.py CommandMission "$1" "$2" "$path" "$3"
}

test_json_format()
{
  python ${path}/examples/jenkins/test_json.py json_test "$1"
}

check_irf_config()
{
  python ${path}/examples/jenkins/test_json.py check_irf_config  "$1" "$path"
}
wait_host()
{
  python ${path}/examples/jenkins/test_json.py wait_host  "$1"
}
make_irf_interfaces_conf()
{
  python ${path}/examples/jenkins/test_json.py make_irf_interfaces_conf  "$1" "$path"
}