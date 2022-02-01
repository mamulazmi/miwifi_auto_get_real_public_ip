import os
import re
import sys
import time
import utils
import requests
import ipaddress
import CloudFlare
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# get device_id and key for login()
req = requests.get('http://{}/cgi-bin/luci/web/home'.format(os.getenv('ROUTER_IP')))
html_body = req.text
device_id = re.findall("(?<=deviceId = ').*(?=';)", html_body)[0]
key = re.findall("(?<=key: ').*(?=',)", html_body)[0]

# login for getting wan_ip(Public IP)
mi_wifi = utils.MiWiFi(host='http://{}'.format(os.getenv('ROUTER_IP')), password=os.getenv('ROUTER_PASSWORD'))
mi_wifi.login(device_id, os.getenv('ROUTER_PASSWORD'), key)
    

def get_current_ip():
    global mi_wifi
    pppoe_dict = mi_wifi.runAction('pppoe_status')
    wan_ip = pppoe_dict['ip']['address']
    
    return ipaddress.IPv4Address(wan_ip)


def start():
    global mi_wifi
    
    lastIp = str(get_current_ip())
    
    while get_current_ip().is_private:
        mi_wifi.runAction('pppoe_stop')
        time.sleep(1)
        mi_wifi.runAction('pppoe_start')
        time.sleep(5)
        
    currentIp = str(get_current_ip())
        
    if lastIp != currentIp:
        update_cloudflare_dns(currentIp)
    
    print("last IP : ", lastIp)
    print("Current IP : ", currentIp)
    
    
def reload():
    global mi_wifi
    
    mi_wifi.runAction('pppoe_stop')
    time.sleep(1)
    mi_wifi.runAction('pppoe_start')
    time.sleep(5)
    
    return start()

def update_cloudflare_dns(newIp):
    
    print("updating cloudflare...")
    
    cf = CloudFlare.CloudFlare(token=os.getenv('CLOUDFLARE_TOKEN'))
    
    dns_record = {
        'name': os.getenv('CLOUDFLARE_DOMAIN_NAME'),
        'type': 'A',
        'content': newIp,
        'proxied': bool(os.getenv('CLOUDFLARE_DOMAIN_PROXIED'))
    }
    try:
        dns_record = cf.zones.dns_records.put(os.getenv('CLOUDFLARE_ZONE_ID'), os.getenv('CLOUDFLARE_DOMAIN_ID'), data=dns_record)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.dns_records.put %s - %d %s - api call failed' % (os.getenv('CLOUDFLARE_DOMAIN_NAME'), e, e))
    

if __name__ == '__main__':
    try:
        arg = sys.argv
        if arg[1] == 'start':
            start()
        elif arg[1] == 'reload':
            reload()
        elif arg[1] == 'get_ip':
            print(str(get_current_ip()))
        else:
            print('plz enter any correct arg, not: ' + arg[1])
    except IndexError:
        print('Plz ensure that you have input any correct parameter')
