from . import *

class EnvironmenteXistdb30(EnvironmentHTTP, IEnvironment):
  DataDirMount       = '/opt/exist/webapp/WEB-INF/data'
  DataDir            = None
  LogDirMount        = '/var/log/exist'
  LogDir             = None
  AutodeployDirMount = '/opt/exist/autodeploy'
  AutodeployDir      = None

  def __init__(self, conf, owner):
    self.runAsUser = True
    if 'DockerfileDir' not in conf :
      conf['DockerfileDir'] = 'existdb30'
    super(EnvironmenteXistdb30, self).__init__(conf, owner)
    if (
        not 'DataDir' in conf
        or self.owner and (
          not Param.isValidRelPath(conf['DataDir'])
          or not Param.isValidDir(self.BaseDir + '/' + conf['DataDir'])
        )
      ) :
        raise Exception('DataDir is missing or invalid')
    self.DataDir = conf['DataDir']
    if (
        not 'LogDir' in conf
        or self.owner and (
          not Param.isValidRelPath(conf['LogDir'])
          or not Param.isValidDir(self.BaseDir + '/' + conf['LogDir'])
        )
      ) :
        raise Exception('LogDir is missing or invalid')
    self.LogDir = conf['LogDir']
    if 'AutodeployDir' in conf:
      if (self.owner and (
            not Param.isValidRelPath(conf['AutodeployDir'])
            or not Param.isValidDir(self.BaseDir + '/' + conf['AutodeployDir'])
          )
        ) :
          raise Exception('AutodeployDir is missing or invalid')
      self.AutodeployDir = conf['AutodeployDir']
    self.Mounts.append({ "Host" : self.DataDir, "Guest" : self.DataDirMount, "Rights" : "rw" })
    self.Mounts.append({ "Host" : self.LogDir, "Guest" : self.LogDirMount, "Rights" : "rw" })
    if (self.AutodeployDir is not None): self.Mounts.append({ "Host" : self.AutodeployDir, "Guest" : self.AutodeployDirMount, "Rights" : "rw" })

class EnvironmenteXistdb22(EnvironmenteXistdb30, IEnvironment):

  def __init__(self, conf, owner):
    if 'DockerfileDir' not in conf :
      conf['DockerfileDir'] = 'existdb22'
    super(EnvironmenteXistdb22, self).__init__(conf, owner)

class EnvironmenteXistdb31(EnvironmenteXistdb30, IEnvironment):

  def __init__(self, conf, owner):
    if 'DockerfileDir' not in conf :
      conf['DockerfileDir'] = 'existdb31'
    super(EnvironmenteXistdb31, self).__init__(conf, owner)

class EnvironmenteXistdb34(EnvironmenteXistdb30, IEnvironment):

  def __init__(self, conf, owner):
    if 'DockerfileDir' not in conf :
      conf['DockerfileDir'] = 'existdb34'
    super(EnvironmenteXistdb34, self).__init__(conf, owner)

class EnvironmenteXistdb3x(EnvironmenteXistdb30, IEnvironment):

  def __init__(self, conf, owner):
    if 'DockerfileDir' not in conf :
      conf['DockerfileDir'] = 'existdb4x'
    super(EnvironmenteXistdb3x, self).__init__(conf, owner)

class EnvironmenteXistdb4x(EnvironmenteXistdb30, IEnvironment):

  def __init__(self, conf, owner):
    if 'DockerfileDir' not in conf :
      conf['DockerfileDir'] = 'existdb4x'
    super(EnvironmenteXistdb4x, self).__init__(conf, owner)


class EnvironmenteXistdb5x(EnvironmenteXistdb30, IEnvironment):

  def __init__(self, conf, owner):
    self.DataDirMount = '/exist/data'
    self.LogDirMount = '/exist/logs'
    self.AutodeployDirMount = '/exist/autodeploy'
    if 'DockerfileDir' not in conf :
      conf['DockerfileDir'] = 'existdb5x'
    super(EnvironmenteXistdb5x, self).__init__(conf, owner)
