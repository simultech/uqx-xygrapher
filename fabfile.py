from fabric.api import *
from fabric.contrib.console import confirm

verbose = True
env.projectname = 'grapher'
env.activate = 'source /Users/uqadekke/Sites/sources/grapher/env/bin/activate'

def host_type():
    print("Hello world!")
    run('uname -s')

def prepare_deploy():
    func_test()
    func_gitadd("Auto Commit")
    func_gitpush()

#Internal

def func_test():
    if verbose:
        print "Testing project"
    local_ve("./manage.py test "+env.projectname)

def func_gitadd(git_message):
    if verbose:
        print "Git adding"
    local_ve("git add . && git commit -a -m \""+git_message+"\"")

def func_gitpush():
    if verbose:
        print "Pushing to github"
    local_ve("git push")

#Helpers

def local_ve(cmd):
    result = local(env.activate+" && "+cmd, capture=True)
    if result.failed and not confirm("Command failed. Continue anyway?"):
        abort("Aborting at user request.")