import boto3
import random
import time
from instance_manager import new_instance, delete_instance, cleaner, instance_setup

access_key = 'ASIA2JWTJAFB57L2S7AZ'
secret_key = '+aSPnyTspSwYZ1sRqb3pnAJWVXP7xMM1UBUYiViU'
session_token = 'FwoGZXIvYXdzEDgaDHI/yCMEjOvLGDIWeyLIAaIUUCs/5WAXzZvBf7xZQYQ6hDakNSNbOQPjP1qLgk1q0tStbdR/SSxvKbwC7PIqg8nbICrGHaC3MploPwXeC2ZH0TWfMm8XHFzW/m1wFFff8obKa/KpAh13TBE8n1hVybhRmcXwq22UH62kbRZE5IH7z9pDtu36nE2kxNmBLhTsJlnbJtavjUsD0adNvFCaF4CMUO5Rt6sAuc7AirPsU/F14z+D7XwYROJOl61InpRfan2vaBRiLsTOK0gkQmgIix+O1FDN6zj1KKu2laMGMi2/FBoPS6VVyg/G46/6h7AAPZ+TqBf3IuY224PcbghBrnsJSS0l7oSidXtzQYo='
region = 'us-east-1'

group_name = 'Proyecto2 ScalingGroup'
instance_id = 'i-0c815d2e545a64860'
cpu_upper_limit = 0.7
cpu_lower_limit = 0.3
max_instances = 5
min_instances = 2
instance_list = []

ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    aws_session_token=session_token,
    region_name=region,
)

autoscaling_client = boto3.client(
    'autoscaling',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    aws_session_token=session_token,
    region_name=region,
)

cleaner(ec2_client, autoscaling_client, group_name)
id1, id2 = instance_setup(ec2_client, autoscaling_client, group_name)
instance_list.append(id1)
instance_list.append(id2)
current_instances = 2


while True:
    cpu_avg = random.random()
    print("CPU average: " + str(cpu_avg) + "\n")
    if cpu_avg > cpu_upper_limit and current_instances < max_instances:

        print("Creamos nueva instancia\n")
        instance, _ = new_instance(ec2_client, autoscaling_client, "", group_name)
        instance_list.append(instance)
        current_instances += 1
        print("Instancias activas: " + str(current_instances) + "\n")

    elif cpu_avg < cpu_lower_limit and current_instances > min_instances:

        print("Eliminamos una instancia\n")
        instance_to_delete = instance_list.pop(0)
        delete_instance(ec2_client, autoscaling_client, instance_to_delete, group_name)
        current_instances -= 1
        print("Instancias activas: " + str(current_instances) + "\n")

    print("-------------------------------------------------")
    time.sleep(10)
