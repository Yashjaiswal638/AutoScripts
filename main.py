import random

from aws_resources import *
from backup import *
from jobs import *
from clone import *
from delete import *

if __name__ == '__main__':
    ip = "13.233.133.5"
    backupPolicy = "AP-CA-SR"
    gn = "sarCA6"
    state = 'BACKUPCOPY'
    acc = ''
    checkName = backupName(ip, gn)
    if checkName == 200:
        check = associate(ip, gn, ec2('Yash'), rds('Yash'), alb('Yash'))
        if check == 200:
            submitBackup(ip, gn, backupPolicy)
    if jobCompletion(ip, gn, state):
        instance = ec2('Yash')
        db = rds('Yash')
        instanceId = (random.choice(instance)['instanceId'])
        dbId = random.choice(db)
        if 'CA' in backupPolicy:
            acc = 'YJ'
        else:
            acc = 'NIM-CB'
        if listBackup(ip, gn, instanceId, acc):
            print('Backup Available')
            if 'CA' in backupPolicy:
                cloneEc2CA(ip, gn, instanceId)
                if jobCompletion(ip, gn, 'CLONEAMI'):
                    print('Cloning Successfull')
                    cloneRdsCA(ip, gn, dbId)
                    if jobCompletion(ip, gn, 'RDSINSTANCECLONE'):
                        print('Cloning Successfull')
                        groupCloneCA(ip, gn)

            else:
                cloneEc2(ip, gn, instanceId)
        else:
            print('BackUp not Available')
    # deleteBackUp(ip, gn)
    # deldbcloneSA(ip, gn, 'database-test')
    # delcloneSR(ip, gn, 'i-0b17c829ea102d2bd')
