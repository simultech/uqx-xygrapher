from fabric.api import *
from fabric.contrib.console import confirm

verbose = True
env.projectname = 'grapher'
env.git_projectname = 'uqx-xygrapher'
env.remote_projectname = 'xygrapher'

env.local_base = '../..'
env.remote_base = '/var/www/django/'+env.remote_projectname
env.remote_code_dir = env.remote_base+'/src/'+env.git_projectname

env.hosts = ['uqmarkup']

def prepare():
    func_setup()
    func_test()
    func_gitadd()
    func_gitpush()

def deploy():
    with settings(warn_only=True):
        if run("test -d %s" % env.remote_code_dir).failed:
            print "ERROR: NOT CLONED YET"
            #run("git clone user@vcshost:/path/to/repo/.git %s" % env.remote_code_dir)
    with cd(env.remote_code_dir):
        remote_vc("git pull", "Pulling from git","Enter git password: ")

#Internal

def func_setup():
    local_ve("pip freeze > ./setup/requirements.txt", "Freezing requirements")

def func_test():
    local_ve("./manage.py test " + env.projectname, "Testing project")


def func_gitadd():
    git_message = prompt("[Local] Enter Git Commit Message: ","Hotfix")
    if git_message == "":
        git_message = "Anonymous Hotfix"
    local_ve("git add . && git commit -a -m \"" + git_message + "\"", "Git adding", True)


def func_gitpush():
    local_ve("git push", "Pushing to github")


#Helpers

def local_ve(cmd, message, ignoreerror=False):
    if verbose:
        print "[Local] Command: " + message
    with hide('output', 'running', 'warnings'), settings(warn_only=True):
        envcmd = 'source '+env.local_base+'/env/bin/activate'
        result = local(envcmd + " && " + cmd, capture=True)
        if not ignoreerror and result.failed and not confirm("+ Error: " + message + " failed. Continue anyway?"):
            abort("Aborting at user request.")

def remote_vc(cmd, message, premessage=""):
    if verbose:
        print "["+env.host_string+"] Command: " + message
    with hide('output', 'running', 'warnings'), settings(warn_only=True):
        if premessage != "":
            print premessage
        envcmd = 'source '+env.remote_base+'/env/bin/activate'
        result = sudo(envcmd + " && " + cmd)
        if result.failed and not confirm("+ Error: " + message + " failed. Continue anyway?"):
            abort("Aborting at user request.")