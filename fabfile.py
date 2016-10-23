from fabric.api import env
from scripts.ubuntu import *
from scripts.digitalocean import *
from config import USER, PRIVATE_KEY_FILE, HOSTS

env.user = USER
env.key_filename = PRIVATE_KEY_FILE
env.hosts = HOSTS
