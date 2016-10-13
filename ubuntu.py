from fabric.api import sudo

def update():
    sudo("apt-get update")
    sudo("apt-get upgrade -y")
