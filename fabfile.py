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
    local_ve("./manage.py test "+env.projectname, "Testing project")

def func_gitadd(git_message):
    local_ve("git add . && git commit -a -m \""+git_message+"\"", "Git adding")

def func_gitpush():
    local_ve("git push", "Pushing to github")

#Helpers

def local_ve(cmd,message):
    if verbose:
        print "Command: "+message
    with settings(warn_only=True):
        result = local(env.activate+" && "+cmd, capture=True)
        if result.failed and not confirm("Command "+message+" failed. Continue anyway?"):
            abort("Aborting at user request.")