import requests
import json
import urllib3
import time
from dicts import *

urllib3.disable_warnings()


def jobCompletion(ip, gn, state):
    url = f"https://{ip}:9443/common/jobs"
    jobId = ''

    params = {
        "application": "aws",
        "limit": 5,
        "offset": 0
    }

    while True:
        response = requests.get(url, headers=headers, params=params, verify=False)
        res = (json.loads(response.content.decode("utf-8")))
        time.sleep(10)
        for i in range(5):
            if (res['jobDtos'][i]['group_name']) == gn and res['jobDtos'][i]['command'] == state:
                if 'Success' in res['jobDtos'][i]['result']:
                    return 1


def discover(ip):
    url1 = f"https://{ip}:9443/common/application/discover/NIM-CB"

    response = requests.get(url1, headers=headers, verify=False)
    time.sleep(30)
    return (response.status_code)
