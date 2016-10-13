from fabric.api import env
from ubuntu import update

env.user = 'user'
env.key_filename = '/path/to/ssh/key'
env.hosts = ['host.test.com']
