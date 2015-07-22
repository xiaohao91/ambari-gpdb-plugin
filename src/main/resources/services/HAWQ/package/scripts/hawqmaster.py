#!/usr/bin/env python
from resource_management import *
import hawq
import active_master_helper

class HawqMaster(Script):
  def install(self, env):
    self.install_packages(env)
    self.configure(env)

  def configure(self, env):
    import params
    env.set_params(params)
    hawq.common_setup(env)
    hawq.master_configure(env)
    hawq.system_verification(env, "master")

  def start(self, env):
    self.configure(env)
    # Identify active hawq master
    if active_master_helper.is_localhost_active_master():
      # Execute master port check to identify port conflicts
      hawq.check_port_conflict()
      # Execute hawq start
      hawq.start_hawq(env)
    else:
      # Ignore port check for standby as it will lead to port conflicting issues during restart
      Logger.info("This host is not the active master, skipping requested operation.")

  def stop(self, env):
    hawq.stop_hawq(env)

  def status(self, env):
    import status_params
    check_process_status(status_params.pid_hawqmaster)

if __name__ == "__main__":
  HawqMaster().execute()
