from resource_management import *

def init(env):
  import params
  File("{0}/pxf-env.sh".format(params.pxf_conf_dir),
     content=Template("pxf-env.j2"))

  File("{0}/pxf-private.classpath".format(params.pxf_conf_dir),
       content=Template("pxf-private-classpath.j2"))

  if params.security_enabled:
    params.config['configurations']['pxf-site']['pxf.service.kerberos.principal'] = params._pxf_principal_name

  XmlConfig("pxf-site.xml",
    conf_dir=params.pxf_conf_dir,
    configurations=params.config['configurations']['pxf-site'],
    configuration_attributes=params.config['configuration_attributes']['pxf-site'])

  if params.security_enabled:
    command  = "chown %s:%s %s &&" % (params.pxf_user, params.user_group, params.pxf_keytab_file)
    command += "chmod 440 %s" % (params.pxf_keytab_file)
    Execute(command, timeout=600)

  command = "service pxf-service init && usermod -s /bin/bash %s" % params.pxf_user
  Execute(command, timeout=600)

  # Ensure that instance directory is owned by pxf:pxf. 
  # Directory() functions takes care of the permission only while executing makedirs, however if the directories are already available, it doesnot changes the permission, thus using chown here.
  # This behavior appears to be fixed in Ambari 2.0.
  command = "chown {0}:{0} -R {1}".format(params.pxf_user, params.pxf_instance_dir)
  Execute(command, timeout=600)

  if System.get_instance().os_family == "suse":
    command = "usermod -A {0} pxf".format(params.hdfs_superuser_group)
  else:
    command = "usermod -a -G {0} pxf".format(params.hdfs_superuser_group)
  Execute(command, timeout=600)

def start(env):
  import params
  command = "service pxf-service restart"
  Execute(command, timeout=600)

def stop(env):
  import params
  command = "service pxf-service stop"
  Execute(command, timeout=600)

def status(env):
  import params
  import httplib
  import re
  # check tcServer process
  check_process_status(params.tcserver_pid_file)

  # check PXF web service
  h=httplib.HTTPConnection('localhost', 51200)
  try:
    h.request("GET","/pxf/v1")
    response = h.getresponse()
    data = response.read()
    obj = re.match(r'.*Wrong version v[0-9]+, supported version is v[0-9]+', data)
    if not obj:
      Logger.debug("PXF service is failing with message:\n{0}".format(data))
      raise ComponentIsNotRunning()
  except:
    Logger.debug("Connection failed to PXF service at localhost:51200")
    raise ComponentIsNotRunning()
    
