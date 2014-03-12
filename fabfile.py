from fabric.api import *

env.projectname = 'grapher'
env.activate = 'source /Users/uqadekke/Sites/sources/grapher/env/bin/activate'

def host_type():
    print("Hello world!")
    run('uname -s')

def prepare_deploy():
    git_message = "Auto Commit"
    print("Git Push and Commit")
    local_ve("./manage.py test "+env.projectname)
    local_ve("git add . && git commit -a -m \""+git_message+"\"")
    local_ve("git push")

def local_ve(cmd):
    print "DOING: "+cmd
    local(env.activate+" && "+cmd)