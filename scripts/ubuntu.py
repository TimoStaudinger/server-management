from fabric.api import sudo, task

@task
def update():
    sudo("apt-get update")
    sudo("apt-get upgrade -y")
