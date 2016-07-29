import codecs
import re
from . import *


class EnvironmentDrupal8(EnvironmentPHP, IEnvironment):
    skipDocumentRoot = True
    Version = '1.0'

    def __init__(self, conf, owner):
        if 'DockerfileDir' not in conf:
            conf['DockerfileDir'] = 'http_drupal8'
        self.ImitateHTTPS = self.HTTPS

        super(EnvironmentDrupal8, self).__init__(conf, owner)

        if not 'SitesDir' in conf or not Param.isValidRelPath(conf['SitesDir']) or not Param.isValidDir(
                                self.BaseDir + '/' + conf['SitesDir']):
            raise Exception('SitesDir is missing or invalid')
        self.Mounts.append({"Host": conf['SitesDir'], "Guest": '/var/www/html/sites', "Rights": "rw"})

        if not 'ModulesDir' in conf or not Param.isValidRelPath(conf['ModulesDir']) or not Param.isValidDir(
                                self.BaseDir + '/' + conf['ModulesDir']):
            raise Exception('ModulesDir is missing or invalid')
        self.Mounts.append({"Host": conf['ModulesDir'], "Guest": '/var/www/html/modules', "Rights": "rw"})

        if not 'ThemesDir' in conf or not Param.isValidRelPath(conf['ThemesDir']) or not Param.isValidDir(
                                self.BaseDir + '/' + conf['ThemesDir']):
            raise Exception('ThemesDir is missing or invalid')
        self.Mounts.append({"Host": conf['ThemesDir'], "Guest": '/var/www/html/themes', "Rights": "rw"})

        if not 'ProfilesDir' in conf or not Param.isValidRelPath(conf['ProfilesDir']) or not Param.isValidDir(
                                self.BaseDir + '/' + conf['ProfilesDir']):
            raise Exception('ProfilesDir is missing or invalid')
        self.Mounts.append({"Host": conf['ProfilesDir'], "Guest": '/var/www/html/profiles', "Rights": "rw"})

        if not 'LibrariesDir' in conf or not Param.isValidRelPath(conf['LibrariesDir']) or not Param.isValidDir(
                                self.BaseDir + '/' + conf['LibrariesDir']):
            raise Exception('LibrariesDir is missing or invalid')
        self.Mounts.append({"Host": conf['LibrariesDir'], "Guest": '/var/www/html/libraries', "Rights": "rw"})


    # as Drupal environment does not have DocumentRoot it is not clear what
    # should be a base dir for aliases
    def processAliases(self, conf):
        pass

    def runHooks(self, verbose):
        super(EnvironmentPHP, self).runHooks(verbose)

        if verbose:
            print('    Setting up drupal permissions')
        self.runProcess(
            ['docker', 'exec', self.Name, 'chown', '-R', self.UserName + ':' + self.UserName, '/var/www/html'], verbose,
            '', 'Setting up permissions failed')

    def adjustVersion(self, dockerfile):
        hashes = {
            '0.0': '92ce9a54fa926b58032a4e39b0f9a9f1',
            '0.1': '423cc4d28da066d099986ac0844f6abb',
            '0.2': '9c39dec82c6d1a6d2004c30b11fb052e',
            '0.3': '7d5f5278a870b8f4a29cda4fe915d619',
            '0.4': '7516dd4c18415020f80f000035e970ce',
            '0.5': 'c13a69b0f99d70ecb6415d77f484bc7f',
            '0.6': '952c14d46f0b02bcb29de5c3349c19ee',
            '1.0': 'a6bf3c366ba9ee5e0af3f2a80e274240',
            '1.1': '529f3d72964c612695f68e0a6078b8ae',
            '1.2': '91fdfbd1c28512e41f2a61bf69214900',
            '1.3': 'f2eef421c2a0610b32519f8f2e094b7c',
            '1.4': '8c07b855ffd028124eb8848526abf4d9',
            '1.5': '0b30a3711d922c5348d6119e5124243b',
            '1.6': 'f3fdd2f9266938c2c7afc091e8d6e6d1',
            '1.7': '19e95079e50dd3c19222b91ef1b57036'
        }

        if self.Version not in hashes:
            raise Exception('Version %s is not supported' % self.Version)

        with codecs.open(dockerfile, mode='r', encoding='utf-8') as df:
            commands = df.read()
            commands = re.sub('@VERSION@', '8.' + self.Version, commands)
            commands = re.sub('@HASH@', hashes[self.Version], commands)
        with codecs.open(dockerfile, mode='w', encoding='utf-8') as df:
            df.write(commands)
