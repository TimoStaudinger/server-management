from fabric.api import run

def update():
    run("sudo apt-get update")
    run("sudo apt-get upgrade -y")
