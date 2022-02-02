#!/usr/bin/env python3

import json
import os
import subprocess
import prometheus_client as prom
import time



def kubent(helm2, helm3, cluster):
    cmd = ['kubent', '-o', 'json', '--helm2={}'.format(str(helm2)), '--helm3={}'.format(str(helm3)), '--cluster={}'.format(str(cluster))]

    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    result = json.loads(result.stdout)

    return result

if __name__ == "__main__":
    sleepTime = os.getenv('DEPRECATION_CHECK_WAIT_TIME', "604800")
    metricsPort = os.getenv('METRICS_PORT', "9092")
    metricsListenAddres = os.getenv('METRICS_IP', "0.0.0.0")


    prom.start_http_server(int(metricsPort), metricsListenAddres)

    gauge = prom.Gauge(
        "deprecation_in_cluster", 
        'Deprecation metric',
        ['name','namespace','kind','api_version','replace_with','since','source']
    )

    while True:
        for warning in kubent(True, False, False):
            value=(warning['RuleSet']).split()[-1]
            
            
            gauge.labels(
                warning['Name'],
                warning['Namespace'].replace('<undefined>','GLOBAL'),
                warning['Kind'],
                warning['ApiVersion'],
                warning['ReplaceWith'],
                warning['Since'],
                "helm2"
            
            ).set(value)


        for warning in kubent(False, True, False):
            value=(warning['RuleSet']).split()[-1]
            
            
            gauge.labels(
                warning['Name'],
                warning['Namespace'].replace('<undefined>','GLOBAL'),
                warning['Kind'],
                warning['ApiVersion'],
                warning['ReplaceWith'],
                warning['Since'],
                "helm3"
            
            ).set(value)

        for warning in kubent(False, False, True):
            value=(warning['RuleSet']).split()[-1]
            
            
            gauge.labels(
                warning['Name'],
                warning['Namespace'].replace('<undefined>','GLOBAL'),
                warning['Kind'],
                warning['ApiVersion'],
                warning['ReplaceWith'],
                warning['Since'],
                "cluster"
            
            ).set(value)

        time.sleep(int(sleepTime))