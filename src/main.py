parser = argparse.ArgumentParser(description='Script for maintiaining docker images and containers')
parser.add_argument('-p', '--project', action = 'append', nargs = '*', required = False, help = 'Project whose environments should be processed')
parser.add_argument('-e', '--environment', action = 'append', nargs = '*', required = False, help = 'Names of environments to proccess')
parser.add_argument('-a', '--action', action = 'store', nargs = 1, required = False, choices = ['check', 'build', 'run', 'clean', 'enter-as-root', 'enter', 'logs'],  help = 'Action to perform')
parser.add_argument('-v', '--verbose', action = 'store_true', required = False,  help = 'Enable verbose output')
args = parser.parse_args()
if args.project is None :
  args.project = [[]]
args.project = reduce(lambda x, y: x + y, args.project)
if args.environment is None :
  args.environment = [[]]
args.environment = reduce(lambda x, y: x + y, args.environment)

print 'Loading config...'
configuration = Configuration()

print 'Checking conflicts between environments...'
configuration.check()

for i in configuration.findEnvironments([], [], True):
  print '  ' + i.Name + ' ' + str(i.ready)
  
if args.action is None or args.action.count('build') > 0 :
  print 'Building images...'
  configuration.buildImages(args.project, args.environment, args.verbose)

if args.action is None or args.action.count('run') > 0 :
  print 'Running containers...'
  configuration.runContainers(args.project, args.environment, args.verbose)

  print 'Running hooks...'
  # give container(s) time to start before executing hooks
  time.sleep(5)
  configuration.runHooks(args.project, args.environment, args.verbose)

if not args.action is None and args.action.count('clean') > 0 :
  configuration.clean(args.project, args.environment, args.verbose)

if not args.action is None :
  if len(args.action) != 1 :
    print "  Please choose exactly one environment"
  else:
    if   args.action.count('enter-as-root') > 0 or args.action.count('enter') > 0 :
      print 'Running console...'
      configuration.runConsole(args.project, args.environment[0], args.action[0])
    elif args.action.count('logs') > 0 :
      print 'Printing logs...'
      configuration.showLogs(args.project, args.environment[0])
