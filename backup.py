import requests
import json
import urllib3
from dicts import *

urllib3.disable_warnings()


def backupName(ip, gn):
    url = f"https://{ip}:9443/aws/backupgroup"
    payload = {
        'account': 'NIM-CB',
        'associationType': 'LIST',
        'groupName': gn,
        'objectValue': 'Instance',
        'region': 'ap-south-1',
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    return response.status_code


def associate(ip, gn, ec2, rds, alb):
    instances = ec2
    rdsIns = rds
    lbs = alb


    url = f"https://{ip}:9443/aws/backupgroup/associate"
    params = {
        "groupName": gn,
        "associationType": "LIST",
        "instances": instances,
        "rdsInstances": rdsIns,
        "loadBalancer": lbs
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(params), verify=False)
    return (response.status_code)


def submitBackup(ip, gn, backupPolicy):
    url = f"https://{ip}:9443/aws/backupgroup"
    params = {
        "account": "NIM-CB",
        "associationType": "LIST",
        "groupName": gn,
        "objectValue": "Instance",
        "policyMappings": [{"backupPolicy": backupPolicy, "schedulePolicy": "Run Now"}],
        "region": "ap-south-1"
    }
    response = requests.request("PUT", url, headers=headers, data=json.dumps(params), verify=False)
    print(response.status_code)


def listBackup(ip, gn, id, acc):
    url = f"https://{ip}:9443/aws/backup/secondary"

    params = {
        'limit': 2,
        'offset': 0,
        'account': acc,
        'groupName': gn,
        'objectId': id
    }

    response = requests.get(url, headers=headers, params=params, verify=False)
    return json.loads(response.content.decode("utf-8"))['totalBackup']


def deleteBackUp(ip, gn):
    url3 = f"https://{ip}:9443/aws/backupgroup/{gn}"

    # this is going as query-string parameter
    params = {
        "keep_backup": "false",
        "account": "NIM-CB",
    }

    response = requests.delete(url3, headers=headers, params=params, verify=False)
    print('Delete Initiated')