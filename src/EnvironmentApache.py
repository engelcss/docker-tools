class EnvironmentApache(EnvironmentHTTP, IEnvironment):
  DocumentRootMount  = '/var/www/html'
  DocumentRoot       = None
  AllowOverride      = 'All'
  Options            = 'None'
  Aliases            = None

  def __init__(self, conf, owner):
    self.Aliases = []
    if 'DockerfileDir' not in conf :
      conf['DockerfileDir'] = 'http_http'
    super(EnvironmentApache, self).__init__(conf, owner)
    self.Ports = [{ "Host" : HTTPReverseProxy.getPort(), "Guest" : 80 , "Type" : "HTTP", "ws" : []}]

    if not Param.isValidDomain(self.ServerName) :
      raise Exception('ServerName is missing or invalid')

    if (
      not 'DocumentRoot' in conf 
      or self.owner and (
        not Param.isValidRelPath(conf['DocumentRoot'])
        or not Param.isValidDir(self.BaseDir + '/' + conf['DocumentRoot'])
      )
    ) :
      raise Exception('DocumentRoot is missing or invalid')
    self.DocumentRoot = conf['DocumentRoot']
    self.Mounts.append({ "Host" : self.DocumentRoot, "Guest" : self.DocumentRootMount, "Rights" : "rw" })

    if 'AllowOverride' in conf :
      self.processAllowOverride(conf['AllowOverride'])

    if 'Options' in conf :
      self.processOptions(conf['Options'])

    if 'Aliases' in conf :
      self.processAliases(conf['Aliases'])

  def processAllowOverride(self, conf):
    dictionary = ['All', 'AuthConfig', 'FileInfo', 'Indexes', 'Limit', 'Options']
    
    if not isinstance(conf, list):
      if not isinstance(conf, basestring):
        raise Exception('AllowOverride is not a string nor list')
      conf = [conf]

    self.AllowOverride = ''
    for opt in conf:
      dictionary.index(opt)
      self.AllowOverride += ' ' + opt

  def processOptions(self, conf):
    dictionary = ['All', 'ExecCGI', 'FollowSymLinks', 'Includes', 'MultiViews', 'SymLinksIfOwnerMatch']
    
    if not isinstance(conf, list):
      if not isinstance(conf, basestring):
        raise Exception('Options is not a string nor list')
      conf = [conf]

    self.Options = ''
    for opt in conf:
      dictionary.index(opt)
      self.Options += ' ' + opt

  def processAliases(self, conf):
    if not isinstance(conf, list) :
      conf = [conf]

    for alias in conf:
      if not isinstance(alias, dict) :
        raise Exception('Alias definition is not a dictionary')
      if not 'Alias' in alias or not Param.isValidAlias(alias['Alias']) :
        raise Exception('Alias name is missing or invalid')
      if (
        not 'Path' in alias 
        or self.owner and not (
          Param.isValidAbsPath(alias['Path']) 
          or Param.isValidRelPath(alias['Path']) and (
            Param.isValidDir(self.BaseDir + '/' + self.DocumentRoot + '/' + alias['Path']) 
            or Param.isValidFile(self.BaseDir + '/' + self.DocumentRoot + '/' + alias['Path'])
          )
        )
      ) :
        raise Exception('Alias path is missing or invalid')
    self.Aliases = conf

  def runHooks(self, verbose):
    super(EnvironmentApache, self).runHooks(verbose)

    if verbose :
      print '    Configuring Apache in guest'

    self.apacheConfigure()
    self.apacheRestart(verbose)

  def apacheConfigure(self):
    vhFile = self.getApacheVHConfFile()
    vhFile.write(self.guestVHTemplate.format(
      ServerName = self.ServerName,
      ServerAlias = self.getServerAlias(),
      UID = '#' + str(self.UID),
      GID = '#' + str(self.GID),
      DocumentRootMount = self.DocumentRootMount,
      AllowOverride = self.AllowOverride,
      Options = self.Options,
      Aliases = self.getAliases()
    ))
    vhFile.close()

  def apacheRestart(self, verbose):
    self.runProcess(['docker', 'exec', self.Name, 'supervisorctl', 'restart', 'apache2'], verbose, '', 'Apache restart failed')

  def getDockerOpts(self):
    dockerOpts = super(EnvironmentApache, self).getDockerOpts()
    dockerOpts += ['--cap-add=SYS_NICE', '--cap-add=DAC_READ_SEARCH']
    return dockerOpts

  def getApacheVHConfFile(self):
    vhFileName = self.DockerMntBase + '/' + self.Name + '/etc/apache2/sites-enabled/000-default.conf'
    vhFile = open(vhFileName, 'w')
    return vhFile

  def getAliases(self):
    aliases = ''
    for alias in self.Aliases:
      aliases += 'Alias ' + alias['Alias'] + ' ' + self.DocumentRootMount + '/' + alias['Path'] + '\n'
    return aliases

  def getGuestHomeDir(self):
    return '/var/www/html'

  guestVHTemplate = """
<VirtualHost *:80>
  ServerName {ServerName}
  DocumentRoot {DocumentRootMount}
  ServerAlias {ServerAlias}
  AssignUserID {UID} {GID}

  <Directory {DocumentRootMount}>
    Require all granted
    AllowOverride {AllowOverride}
    Options {Options}
  </Directory>

  {Aliases}
</VirtualHost>   
"""

