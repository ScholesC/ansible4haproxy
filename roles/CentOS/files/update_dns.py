#!/usr/bin/env python3
'''
script to update dns record in cloudflare
'''
import os
import json
import requests

def get_record_id(dns_name, zone_id, token):
    '''
    get record id in cloudflare
    '''
    resp = requests.get(
        f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records',
        headers={
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        })
    if not json.loads(resp.text)['success']:
        return None
    domains = json.loads(resp.text)['result']
    for domain in domains:
        if dns_name == domain['name']:
            return domain['id']
    return None


def update_dns_record(dns_name, zone_id, token, dns_id, my_ip, proxied=False):
    '''
    update dns record
    '''
    resp = requests.put(
        f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_id}',
        json={
            'type': 'A',
            'name': dns_name,
            'content': my_ip,
            'proxied': proxied
        },
        headers={
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        })
    if not json.loads(resp.text)['success']:
        return False
    return True


def valid_ip(address):
    '''
    validte ip address
    '''
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except Exception:
        return False


def get_pub_ip():
    '''
    find out pub ip
    '''
    ext_ip = ''
    ext_ip_url = 'https://ifconfig.co/json'
    r = requests.get(ext_ip_url)
    if r.status_code == 200:
        ext_ip = r.json()['ip']
    return ext_ip


def main():
    '''
    api token
    '''
    zone_id = '09ab87df4fef66e1adb5e4f39b4fbb41'
    dns_name = 'shop.buytheworld.shop'
    proxied = False
    pub_ip = get_pub_ip
    token = os.environ['CFTOKEN']
    if not token:
        print('failed to find token.')
    api_token = token
    if valid_ip(pub_ip):
        dns_id = get_record_id(dns_name, zone_id, api_token)
        if update_dns_record(dns_name, zone_id, api_token, dns_id, pub_ip, proxied):
            print(f"succeed to update {dns_name} with {pub_ip}")
        else:
            print(f"failed to update {dns_name} with {pub_ip}")

    else:
        print(f"{pub_ip} is not valid ip address")


if __name__ == '__main__':
    main()
