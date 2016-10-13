from fabric.api import env
from scripts.ubuntu import *
from scripts.digitalocean import *
from config import USER, KEY_FILE, HOSTS

env.user = USER
env.key_filename = KEY_FILE
env.hosts = HOSTS
