from instance_manager import create_instance, terminate_instance, cleaner, instance_setup
from dotenv import load_dotenv
import os
import boto3
import random
import time

load_dotenv()
access_key = os.environ.get('AWS_ACCESS_KEY')
secret_key = os.environ.get('AWS_SECRET_KEY')
session_token = os.environ.get('AWS_SESSION_TOKEN')
region = os.environ.get('REGION')

cpu_lower_limit = float(os.environ.get('CPU_LOWER_LIMIT'))
cpu_upper_limit = float(os.environ.get('CPU_UPPER_LIMIT'))
min_instances = int(os.environ.get('MIN_INSTNACES'))
max_instances = int(os.environ.get('MAX_INSTANCES'))
instance_list = []

ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    aws_session_token=session_token,
    region_name=region,
)

cleaner(ec2_client)
id1, id2 = instance_setup(ec2_client)
instance_list.append(id1)
instance_list.append(id2)
current_instances = 2

while True:
    cpu_avg = random.random()
    print("CPU average: " + str(cpu_avg) + "\n")
    if cpu_avg > cpu_upper_limit and current_instances < max_instances:

        print("Creamos nueva instancia\n")
        instance = create_instance(ec2_client)
        instance_list.append(instance)
        current_instances += 1
        print("Instancias activas: " + str(current_instances) + "\n")

    elif cpu_avg < cpu_lower_limit and current_instances > min_instances:

        print("Eliminamos una instancia\n")
        instance_to_delete = instance_list.pop(0)
        terminate_instance(ec2_client, instance_to_delete)
        current_instances -= 1
        print("Instancias activas: " + str(current_instances) + "\n")

    print("-------------------------------------------------")
    time.sleep(15)
