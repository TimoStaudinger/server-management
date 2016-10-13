from dopy.manager import DoManager
from fabric.api import task
from fabric.contrib.console import confirm
from config import DIGITAL_OCEAN_TOKEN
from util import print_table

do = DoManager(None, DIGITAL_OCEAN_TOKEN, api_version=2)

def get_sizes():
    return print_sizes(sorted(do.sizes(), key=lambda size: size['vcpus']))

def get_images():
    images = filter(lambda image: image['slug'] is not None, do.all_images())
    return sorted(images, key=lambda image: image['slug'])

def print_images(images):
    print_table(images, ['slug', 'name', 'type'])

def print_sizes(sizes):
    print_table(sizes, ['vcpus', 'memory', 'disk'])

def select_image():
    images = filter(lambda image: image['slug'] is not None, get_images())
    ubuntu_images = filter(lambda image: image['slug'].startswith('ubuntu'), images)
    latest_ubuntu = sorted(ubuntu_images, key=lambda image: image['slug'], reverse=True)[0]['slug']
    if confirm('Use image {}'.format(latest_ubuntu)):
        return latest_ubuntu
    else:
        print_images(images)
        while True:
            selected_image = input('Image Key: ')
            if selected_image < len(images):
                image = images[selected_image]['slug']
                if confirm(image):
                    return image
            else:
                print('Image {} not found'.format(selected_image))

def select_size():
    sizes = do.sizes()
    ubuntu_images = filter(lambda image: image['slug'].startswith('ubuntu'), images)
    latest_ubuntu = sorted(ubuntu_images, key=lambda image: image['slug'], reverse=True)[0]['slug']
    if confirm('Use image {}'.format(latest_ubuntu)):
        return latest_ubuntu
    else:
        print_images(images)
        while True:
            selected_image = input('Image Key: ')
            if selected_image < len(images):
                image = images[selected_image]['slug']
                if confirm(image):
                    return image
            else:
                print('Image {} not found'.format(selected_image))

@task
def do_list():
    droplets = do.all_active_droplets()
    print "{:<3} {:<30} {:<10} {:<15}".format('Key', 'Name','Status','IP')
    for k, droplet in enumerate(droplets):
        print "{:<3} {:<30} {:<10} {:<15}".format(k, droplet['name'], droplet['status'], droplet['ip_address'])

@task
def do_images():
    print_images(get_images())

@task
def do_sizes():
    print_sizes(sorted(do.sizes(), key=lambda size: size['vcpus']))

@task
def do_create():
    image = select_image()
