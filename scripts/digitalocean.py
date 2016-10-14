import sys
from time import sleep
from dopy.manager import DoManager
from fabric.api import task, sudo
from fabric.contrib.console import confirm
from config import DIGITAL_OCEAN_TOKEN
from util import print_table

do = DoManager(None, DIGITAL_OCEAN_TOKEN, api_version=2)

def get_sizes():
    return sorted(do.sizes(), key=lambda size: size['vcpus'])

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
            selected_image = input('Image key: ')
            if selected_image < len(images):
                image = images[selected_image]['slug']
                if confirm(image):
                    return image
            else:
                print('Image {} not found'.format(selected_image))

def select_size():
    sizes = get_sizes()
    print_sizes(sizes)
    while True:
        selected_size = input('Size key: ')
        if selected_size < len(sizes):
            size = sizes[selected_size]['slug']
            if confirm(size):
                return size
        else:
            print('Size {} not found'.format(selected_size))

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
def do_create(name = None, size = None, image = None):
    if size == None:
        size = select_size()
    if image == None:
        image = select_image()
    if name == None:
        name = raw_input('Droplet name: ')
    region = 'nyc1'

    droplet = do.new_droplet(name, size, image, region)
    sys.stdout.write('Creating droplet {}...'.format(name))
    sys.stdout.flush()

    while True:
        status = do.show_droplet(droplet['id'])['status']
        if status == 'active':
            break

        sys.stdout.write('.')
        sys.stdout.flush()
        sleep(1)

    print()
    print('Droplet {} created successfully'.format(droplet['id']))
    return droplet['id']

@task
def do_mount_volume(volume):
    sudo('parted /dev/disk/by-id/scsi-0DO_Volume_{} mklabel gpt'.format(volume))
    sudo('parted -a opt /dev/disk/by-id/scsi-0DO_Volume_{} mkpart primary ext4 0\% 100\%'.format(volume))
    sudo('mkfs.ext4 /dev/disk/by-id/scsi-0DO_Volume_{}-part1'.format(volume))
    sudo('mkdir -p /mnt/{}-part1'.format(volume))
    sudo('echo "/dev/disk/by-id/scsi-0DO_Volume_{}-part1 /mnt/{}-part1 ext4 defaults,nofail,discard 0 2" | tee -a /etc/fstab'.format(volume, volume))
    sudo('mount -a')

    # @task
    # def do_unmount_volume(volume):
    #
