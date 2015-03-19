from resource_management.libraries.functions.version import format_stack_version, compare_versions
from resource_management import *

config = Script.get_config()

hdfs_superuser_group = config["configurations"]["hdfs-site"]["dfs.permissions.superusergroup"]
pxf_user = "pxf"
user_group = "hadoop"
security_enabled = config['configurations']['cluster-env']['security_enabled']
tcserver_pid_file = "/var/gphd/pxf/pxf-service/logs/tcserver.pid"

pxf_keytab_file = "/etc/security/keytabs/pxf.service.keytab"

stack_name = str(config['hostLevelParams']['stack_name'])
stack_version_unformatted = str(config['hostLevelParams']['stack_version'])
stack_version = format_stack_version(stack_version_unformatted)

#hadoop params
if stack_name == 'HDP' and compare_versions(stack_version, '2.2') >= 0:
  hdfs_client_home = "/usr/hdp/current/hadoop-hdfs-client"
  mapreduce_libs_path = "/usr/hdp/current/hadoop-mapreduce-client"
  hadoop_home = "/usr/hdp/current/hadoop-client"
  hbase_home = "/usr/hdp/current/hbase-client"
  zookeeper_home = "/usr/hdp/current/zookeeper-client"
  hive_home = "/usr/hdp/current/hive-client"
elif stack_name == 'PHD' and compare_versions(stack_version, '3.0') >= 0:
  hdfs_client_home = "/usr/phd/current/hadoop-hdfs-client"
  mapreduce_libs_path = "/usr/phd/current/hadoop-mapreduce-client"
  hadoop_home = "/usr/phd/current/hadoop-client"
  hbase_home = "/usr/phd/current/hbase-client"
  zookeeper_home = "/usr/phd/current/zookeeper-client"
  hive_home = "/usr/phd/current/hive-client"

pxf_home = "/usr/lib/gphd/pxf"
pxf_conf_dir = '/etc/gphd/pxf/conf'
hadoop_conf_dir = "/etc/hadoop/conf"
hive_conf_dir = "/etc/hive/conf"
hbase_conf_dir = "/etc/hbase/conf"

if config["commandType"] == 'EXECUTION_COMMAND':
  pxf_keytab_file = config["configurations"]["pxf-site"]["pxf.keytab.file"]
  _pxf_principal_name = ''
  if security_enabled:
	  _nn_principal_name = config['configurations']['hdfs-site']['dfs.namenode.kerberos.principal']
	  _pxf_principal_name = _nn_principal_name.replace('nn', 'pxf')
	  # e.g. pxf/_HOST@EXAMPLE.COM
  java_home = config["hostLevelParams"]["java_home"]

