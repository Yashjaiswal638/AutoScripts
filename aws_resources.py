import boto3


def ec2(tag):
    ec2 = boto3.resource('ec2')
    instances = ec2.meta.client.describe_instances()

    ins = []
    for instance in instances['Reservations']:
        res = []
        # if len(instance['Instances'][0]['Tags']) == 1:
        for i in range(len(instance['Instances'][0]['Tags'])):
            res.append(instance['Instances'][0]['Tags'][i]['Value'])
            if tag in res:
                ins.append(instance['Instances'][0]['InstanceId'])

    instances = []
    for i in range(len(ins)):
        instances.append({
            "instanceId": ins[i],
            "volumesExcluded": []
        })

    return instances


def rds(tag):
    rdsIns = []
    rds = boto3.client('rds')
    response = rds.describe_db_instances()
    for db in response['DBInstances']:
        if len(db['TagList']) != 0:
            for i in range(len(db['TagList'])):
                if db['TagList'][i]['Key'] == 'user' and db['TagList'][i]['Value'] == tag:
                    rdsIns.append(db['DBInstanceIdentifier'])
    return rdsIns


def alb(tagTest):
    alb = boto3.client('elbv2')

    response = alb.describe_load_balancers()

    lbs = []
    for i in range(len(response['LoadBalancers'])):
        arn = response['LoadBalancers'][i]['LoadBalancerArn']
        res = alb.describe_tags(
            ResourceArns=[
                arn,
            ]
        )
        tag = res['TagDescriptions'][0]['Tags']
        try:
            if tag[0]['Key'] == 'Name' and tag[0]['Value'] == tagTest:
                lbs.append(arn)
        except IndexError:
            pass
    return lbs
