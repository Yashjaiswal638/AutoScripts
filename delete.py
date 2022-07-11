from dicts import *
import requests
import json
import urllib3

urllib3.disable_warnings()

def delcloneSR(ip, gn, id):
    url = f"https://{ip}:9443/aws/backuplist/{gn}/{id}"

    params = {
        'limit': 2,
        'offset': 0,
    }
    response = requests.get(url, headers=headers, params=params, verify=False)
    res = json.loads(response.content.decode('utf-8'))['backups'][0]
    backName = res['backupName']
    accName = res['amazonInstanceBackup']['host']
    region = json.loads(res['amazonInstanceBackup']['backupInventoryMetadata'])['placement']['availabilityZone'][:-1]

    url = f"https://{ip}:9443/aws/listclone"
    params = {
        'backupName': backName,
        'secondary': False,
        'account': accName,
        'region': region,
    }
    response = requests.get(url, headers=headers, params=params, verify=False)
    cloneId = (json.loads(response.content.decode('utf-8'))[-1]['clone_instance_id'])

    url = f"https://{ip}:9443/aws/deleteclone/{cloneId}"
    response = requests.delete(url, headers=headers, verify=False)
    print(response.status_code)


def deldbcloneSA(ip, gn, id):

    url = f"https://{ip}:9443/aws/backuplist/{gn}/{id}"

    params = {
        'objectType': 'RDS',
        'limit': 2,
        'offset': 0,
    }
    response = requests.get(url, headers=headers, params=params, verify=False)
    backId = json.loads(response.content.decode('utf-8'))['backups'][0]['id']

    url = f'https://{ip}:9443/aws/rds/clone/{id}/{backId}'
    response = requests.get(url, headers=headers, verify=False)
    cloneId = (json.loads(response.content.decode('utf-8'))[-1]['clone_instance_id'])

    url = f'https://{ip}:9443/aws/rds/deleteclone/ap-south-1/{cloneId}'
    response = requests.delete(url, headers=headers, verify=False)
    print(response.status_code)


def delincloneCR(ip, gn, id):
    url = f"https://{ip}:9443/aws/backup/secondary"

    params = {
        'limit': 2,
        'offset': 0,
        'account': 'NIM-CB',
        'groupName': gn,
        'objectId': id
    }

    response = json.loads(requests.get(url, headers=headers, params=params, verify=False).content.decode('utf-8'))
    res = response['backups'][0]
    region = res['drRegions'][0]['region']
    zone = res['drRegions'][0]['volumeSnapshotMaps'][0]['zone']
    backName = res['backupName']

    url = f"https://{ip}:9443/aws/listclone"
    params = {
        'backupName': backName,
        'secondary': False,
        'account': 'NIM-CB',
        'region': region,
    }
    response = requests.get(url, headers=headers, params=params, verify=False)
    cloneId = (json.loads(response.content.decode('utf-8'))[-1]['clone_instance_id'])

    url = f"https://{ip}:9443/aws/deleteclone/{cloneId}"
    response = requests.delete(url, headers=headers, verify=False)
    print(response.status_code)


def deldbcloneCR(ip, gn, id):

    url = f"https://{ip}:9443/aws/backup/secondary"

    params = {
        'limit': 2,
        'offset': 0,
        'account': 'NIM-CB',
        'groupName': gn,
        'objectId': id,
        'objectType': 'RDS'
    }

    response = requests.get(url, headers=headers, params=params, verify=False)
    backId = json.loads(response.content.decode('utf-8'))['backups'][0]['id']
    desRegion = json.loads(response.content.decode('utf-8'))['backups'][0]['region']


    url = f'https://{ip}:9443/aws/rds/clone/{id}/{backId}'
    response = requests.get(url, headers=headers, verify=False)
    cloneId = (json.loads(response.content.decode('utf-8'))[-1]['clone_instance_id'])

    url = f'https://{ip}:9443/aws/rds/deleteclone/{desRegion}/{cloneId}'
    response = requests.delete(url, headers=headers, verify=False)
    print(response.status_code)
