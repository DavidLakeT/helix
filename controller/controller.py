import boto3
from instance_manager import list_instances, create_instance, delete_instance, attach_instance, detach_instance

access_key = 'ASIA2JWTJAFBYHHO6PPF'
secret_key = 'zco+T1lLfWPJKcCAhwAlF9vhTZmg0U4sVE+BXLUA'
session_token = 'FwoGZXIvYXdzECAaDLq9LyNQPUxobabgOyLIAYSMsTShG+JRZKKp3M+VkQxEaQKZ1UzCOYHUPzGSJQe23WSeCks1QJlsKP8TouzefZr3kGmWDW/HPWe0zRyvMfEA4hfPU1HRFnAMnMzb9mn5J/MR6xVwYDkaxlxJRjf09FjNEpsVNTWdRlTElmKd3WF09CWrkshfLX/p4jkhdPKAf5PnIKq4tPc/I2DQkM/NLSC214KStp1ENlSS01xbPrdYa1x8m4rC39EkwG7dQJjAnQpWjr+emPmrWkUIpYoWFzmQG2TiHZBgKMCFkKMGMi2JsSDiNIL5V/QRyv9UZLnkQ3CTR5haOa4///8Y29rRLItI0KTb6Sazj3PBtKg='
region = 'us-east-1'

client = boto3.client(
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

# instance_id = 'i-0839fdda4191d0619'
# group_name = 'Proyecto2 ScalingGroup'
# list_instances()
# print("\n")
# instance = create_instance('test_intance2')
# instance_id = instance['Instances'][0]['InstanceId']
# client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
# list_instances()
# response = attach_instance(instance_id, group_name)

# detach_instance(instance_id, group_name)
# delete_instance(instance_id)
