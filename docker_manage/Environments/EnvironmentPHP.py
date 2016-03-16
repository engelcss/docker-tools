from . import *

class EnvironmentPHP(EnvironmentApache, IEnvironment):
  DockerfileDir     = 'http_php'
  UserName          = 'www-data'
  LogDirMount       = '/var/log/apache2'
  ExecDir           = None
  ExecDirMount       = '/var/www/exec'
  ConfigDir         = None
  ConfigDirMount    = '/var/www/config'
  def __init__(self, conf, owner):
    if 'DockerfileDir' not in conf :
      conf['DockerfileDir'] = self.DockerfileDir
    super(EnvironmentPHP, self).__init__(conf, owner)

    if (
      not 'LogDir' in conf
      or self.owner and (
        not Param.isValidRelPath(conf['LogDir'])
        or not Param.isValidDir(self.BaseDir + '/' + conf['LogDir'])
      )
    ) :
      raise Exception('LogDir is missing or invalid')
    self.LogDir = conf['LogDir']

    if 'ExecDir' in conf:
      if (
        self.owner and (
          not Param.isValidRelPath(conf['ExecDir'])
          or not Param.isValidDir(self.BaseDir + '/' + conf['ExecDir'])
        )
      ) :
        raise Exception('ExecDir is invalid')
      self.ExecDir = conf['ExecDir']

    if 'ConfigDir' in conf:
      if (
        self.owner and (
          not Param.isValidRelPath(conf['ConfigDir'])
          or not Param.isValidDir(self.BaseDir + '/' + conf['ConfigDir'])
        )
      ) :
        raise Exception('ConfigDir is invalid')
      self.ConfigDir = conf['ConfigDir']

    self.Mounts.append({ "Host" : self.LogDir, "Guest" : self.LogDirMount, "Rights" : "rw" })
    if (self.ExecDir is not None):
      self.Mounts.append({ "Host" : self.ExecDir, "Guest" : self.ExecDirMount, "Rights" : "rw" })
    if (self.ConfigDir is not None):
      self.Mounts.append({ "Host" : self.ConfigDir, "Guest" : self.ConfigDirMount, "Rights" : "rw" })


