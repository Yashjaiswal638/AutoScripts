from backup import *

urllib3.disable_warnings()


def cloneEc2(ip, gn, id):
    url = f"https://{ip}:9443/aws/backup/secondary"

    params = {
        'limit': 2,
        'offset': 0,
        'account': 'NIM-CB',
        'groupName': gn,
        'objectId': 'i-0b17c829ea102d2bd'
    }

    response = json.loads(requests.get(url, headers=headers, params=params, verify=False).content.decode('utf-8'))
    res = response['backups'][0]
    region = res['drRegions'][0]['region']
    zone = res['drRegions'][0]['volumeSnapshotMaps'][0]['zone']
    backName = res['backupName']
    accName = res['drRegions'][0]['amazonInstanceBackup']['host']
    eniId = json.loads(res['drRegions'][0]['amazonInstanceBackup']['backupInventoryMetadata'])['networkInterfaces'][0][
        'networkInterfaceId']
    subId = 'subnet-0fa1b369df2aee3dc'
    sg = [json.loads(res['drRegions'][0]['amazonInstanceBackup']['backupInventoryMetadata'])['networkInterfaces'][0][
              'groups'][0]['groupId']]

    try :
        iam_arn = (json.loads(res['drRegions'][0]['amazonInstanceBackup']['backupInventoryMetadata'])['iamInstanceProfile'][
        'arn']).find('/')
        iam = json.loads(res['drRegions'][0]['amazonInstanceBackup']['backupInventoryMetadata'])['iamInstanceProfile'][
              'arn'][iam_arn + 1:]
    except TypeError:
        iam = ''
    #
    insType = json.loads(res['drRegions'][0]['amazonInstanceBackup']['backupInventoryMetadata'])['instanceType']
    volId = 'vpc-023425ba38cd4236f'

    url = f'https://{ip}:9443/aws/instance/clone'

    params = {
        'account': accName,
        'availabilityZone': "ap-southeast-1a",
        'backupName': backName,
        'cloneName': backName + '_clone',
        'cloneNicViewModels': [{'srcInterfaceId': eniId, 'subnetId': subId}],
        'securityGroups': sg,
        'srcInterfaceId': eniId,
        'subnetId': subId,
        'enableMonitoring': False,
        'fromSecondary': True,
        'instanceId': id,
        'instanceProfileRoleName': iam,
        'instanceType': insType,
        'keyName': "nimesa-developers",
        'powerOff': False,
        'powerOn': True,
        'preserveIpV4': False,
        'region': region,
        'restoreType': "INSTANT",
        'secondaryDetails': {region: region},
        'swapRoot': False,
        'targetAccount': accName,
        'volumeId': [volId],
    }

    response = requests.post(url, headers=headers, data=json.dumps(params), verify=False)
    print(response.content.decode('utf-8'))


def cloneRds(ip, gn, db):
    url = f"https://{ip}:9443/aws/backup/secondary"

    params = {
        'limit': 2,
        'offset': 0,
        'account': 'NIM-CB',
        'groupName': gn,
        'objectId': db,
        'objectType': 'RDS'
    }

    response = requests.get(url, headers=headers, params=params, verify=False)
    res = json.loads(response.content.decode("utf-8"))['backups'][0]
    backupName = (res['backupIdentifier'])
    desRegion = res['region']
    acc = res['host']
    subnetGrp = 'defvpc'
    port = (json.loads(res['backupInventoryMetadata'])['endpoint']['port'])
    sg = [(json.loads(res['backupInventoryMetadata'])['vpcSecurityGroups'][0]['vpcSecurityGroupId'])]

    grpName = json.loads(res['backupInventoryMetadata'])['dbParameterGroups'][0]['dbParameterGroupName']
    insClass = (json.loads(res['backupInventoryMetadata'])['dbInstanceClass'])

    cloneProp = {
        'account': acc,
        'backupName': backupName,
        'destRegion': desRegion,
        'expiry': 0,
        'fromSecondary': True,
        'targetAccount': acc,
    }

    params = {
        'cloneDBIdentifier': backupName + "-Clone",
        'cloneProperties': cloneProp,
        'copyTagsToSnapshot': False,
        'dbInstanceClass': insClass,
        'dbSubnetGroupName': subnetGrp,
        'deletionProtection': False,
        'enableIAMDatabaseAuthentication': False,
        'multiAz': False,
        'port': port,
        'vpcSecurityGroupIds': ['sg-0c9d36c95562b80ea']
    }

    url = f'https://{ip}:9443/aws/rds/clonedbinstance'

    response = requests.post(url, headers=headers, data=json.dumps(params), verify=False)
    if response.status_code == 200:
        print('RDS Clone Initiated')


def cloneSAR(ip, gn, id):
    url = f"https://{ip}:9443/aws/backuplist/{gn}/{id}"

    params = {
        'limit': 2,
        'offset': 0,
    }
    response = requests.get(url, headers=headers, params=params, verify=False)
    res = json.loads(response.content.decode('utf-8'))['backups'][0]
    backName = res['backupName']
    accName = res['amazonInstanceBackup']['host']
    img = json.loads(res['amazonInstanceBackup']['backupInventoryMetadata'])['imageId']
    insType = json.loads(res['amazonInstanceBackup']['backupInventoryMetadata'])['instanceType']
    region = json.loads(res['amazonInstanceBackup']['backupInventoryMetadata'])['placement']['availabilityZone'][:-1]
    vol = json.loads(res['amazonInstanceBackup']['backupInventoryMetadata'])['blockDeviceMappings'][0]['ebs']['volumeId']

    url = f"https://{ip}:9443/aws/instance/clone"

    params = {
        'account': accName,
        'backupName': backName,
        'cloneName': backName+"-Clone",
        'instanceId': id,
        'instanceType': insType,
        'keyName': "nimesa-developers",
        'powerOff': False,
        'powerOn': True,
        'region': region,
        'restoreType': "INSTANT",
        'swapRoot': False,
        'targetAccount': accName,
        'volumeId': [vol],
    }

    response = requests.post(url, headers=headers, data=json.dumps(params), verify=False)
    print(response.content.decode('utf-8'))


def clonedbSAR(ip, gn, id):
    url = f"https://{ip}:9443/aws/backuplist/{gn}/{id}"

    params = {
        'objectType': 'RDS',
        'limit': 2,
        'offset': 0,
    }
    response = requests.get(url, headers=headers, params=params, verify=False)
    res = json.loads(response.content.decode('utf-8'))['backups'][0]
    backName = res['backupIdentifier']
    accName = res['clones'][0]['host']
    region = json.loads(res['backupInventoryMetadata'])['dbSubnetGroup']['subnets'][0]['subnetAvailabilityZone']['name'][:-1]

    print(accName)
    # print(accName)

    url = f'https://{ip}:9443/aws/rds/clonedbinstance'
    params = {
        'cloneDBIdentifier': backName+"-Clone",
        'cloneProperties': {
        'account': accName,
        'backupName': backName,
        'destRegion': region,
        'expiry': 0,
        'fromSecondary': False,
        'targetAccount': accName,
    },
    'copyTagsToSnapshot': False,
    'deletionProtection': False,
    'enableIAMDatabaseAuthentication': False,
    'port': 3306,
    }
    response = requests.post(url, headers=headers, data=json.dumps(params), verify=False)
    print(response.content.decode('utf-8'))


def cloneEc2CA(ip, gn, id):
    url = f"https://{ip}:9443/aws/backup/secondary"

    params = {
        'limit': 2,
        'offset': 0,
        'account': 'YJ',
        'groupName': gn,
        'objectId': 'i-070d2cc01527ea94f'
    }

    response = json.loads(requests.get(url, headers=headers, params=params, verify=False).content.decode('utf-8'))
    res = response['backups'][0]
    region = res['drRegions'][0]['region']
    zone = res['drRegions'][0]['volumeSnapshotMaps'][0]['zone']
    backName = res['backupName']
    accName = res['drRegions'][0]['amazonInstanceBackup']['host']
    eniId = json.loads(res['drRegions'][0]['amazonInstanceBackup']['backupInventoryMetadata'])['networkInterfaces'][0][
        'networkInterfaceId']
    subId = 'subnet-11d3845d'
    # sg = [json.loads(res['drRegions'][0]['amazonInstanceBackup']['backupInventoryMetadata'])['networkInterfaces'][0][
    #           'groups'][0]['groupId']]
    sg = ['sg-001e1d3108cb46d0a']

    try:
        iam_arn = (
        json.loads(res['drRegions'][0]['amazonInstanceBackup']['backupInventoryMetadata'])['iamInstanceProfile'][
            'arn']).find('/')
        iam = json.loads(res['drRegions'][0]['amazonInstanceBackup']['backupInventoryMetadata'])['iamInstanceProfile'][
                  'arn'][iam_arn + 1:]
    except TypeError:
        iam = ''

    insType = json.loads(res['drRegions'][0]['amazonInstanceBackup']['backupInventoryMetadata'])['instanceType']
    volId = (res['drRegions'][0])['volumeSnapshotMaps'][0]['volumeId']

    url = f'https://{ip}:9443/aws/instance/clone'

    params = {
        'account': accName,
        'availabilityZone': "ap-south-1b",
        'backupName': backName,
        'cloneName': backName + '_clone',
        'cloneNicViewModels': [{'srcInterfaceId': eniId, 'subnetId': subId}],
        'securityGroups': sg,
        'srcInterfaceId': eniId,
        'subnetId': subId,
        'enableMonitoring': False,
        'fromSecondary': True,
        'instanceId': id,
        'instanceProfileRoleName': iam,
        'instanceType': insType,
        'keyName': "nimesa-developers",
        'powerOff': False,
        'powerOn': True,
        'preserveIpV4': False,
        'region': region,
        'restoreType': "INSTANT",
        'secondaryDetails': {region: region},
        'swapRoot': False,
        'targetAccount': accName,
        'volumeId': [volId],
    }

    response = requests.post(url, headers=headers, data=json.dumps(params), verify=False)
    print(response.content.decode('utf-8'))

def cloneRdsCA(ip, gn, db):
    url = f"https://{ip}:9443/aws/backup/secondary"

    params = {
        'limit': 2,
        'offset': 0,
        'account': 'YJ',
        'groupName': gn,
        'objectId': db,
        'objectType': 'RDS'
    }

    response = requests.get(url, headers=headers, params=params, verify=False)
    res = json.loads(response.content.decode("utf-8"))['backups'][0]
    backupName = (res['backupIdentifier'])
    desRegion = res['region']
    acc = res['host']
    subnetGrp = 'default'
    port = (json.loads(res['backupInventoryMetadata'])['endpoint']['port'])
    sg = ['sg-001e1d3108cb46d0a']

    grpName = json.loads(res['backupInventoryMetadata'])['dbParameterGroups'][0]['dbParameterGroupName']
    insClass = (json.loads(res['backupInventoryMetadata'])['dbInstanceClass'])


    cloneProp = {
        'account': acc,
        'backupName': backupName,
        'destRegion': desRegion,
        'expiry': 0,
        'fromSecondary': True,
        'targetAccount': acc,
    }

    params = {
        'cloneDBIdentifier': backupName + "-Clone",
        'cloneProperties': cloneProp,
        'copyTagsToSnapshot': False,
        'dbInstanceClass': insClass,
        'dbSubnetGroupName': subnetGrp,
        'deletionProtection': False,
        'enableIAMDatabaseAuthentication': False,
        'multiAz': False,
        'port': port,
        'vpcSecurityGroupIds': sg
    }

    url = f'https://{ip}:9443/aws/rds/clonedbinstance'

    response = requests.post(url, headers=headers, data=json.dumps(params), verify=False)
    if response.status_code == 200:
        print('RDS Clone Initiated')


def groupCloneCA(ip, gn):
    url = f'https://{ip}:9443/aws/backupgroup/clone/{gn}'

    params = {
        'cloneNetworkSettings': True,
        'drAccount': "YJ",
        'drRegion': "ap-south-1",
        'testDrill': False,
    }

    response = requests.post(url, headers=headers, data=json.dumps(params), verify=False)
    print(response.status_code)