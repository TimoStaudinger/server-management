def do_list():
    from dopy.manager import DoManager
    from config import DIGITAL_OCEAN_TOKEN
    do = DoManager(None, DIGITAL_OCEAN_TOKEN, api_version=2)
    droplets = do.all_active_droplets()
    print "{:<3} {:<30} {:<10} {:<15}".format('Key', 'Name','Status','IP')
    for k, droplet in enumerate(droplets):
        print "{:<3} {:<30} {:<10} {:<15}".format(k, droplet['name'], droplet['status'], droplet['ip_address'])
