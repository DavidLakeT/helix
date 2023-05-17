import boto3

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


def list_instances():
    response = client.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        print("Nombre de la instancia:", tag['Value'])
            else:
                print("Nombre de la instancia: (Sin nombre)")


def create_instance(name):
    return client.run_instances(
        MinCount=1,
        MaxCount=1,
        ImageId='ami-0557a15b87f6559cf',
        InstanceType='t2.micro',
        KeyName='vockey',
        SecurityGroupIds=['default'],
        UserData='',
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': name}]
        }]
    )


def attach_instance(instance_id, group_name):
    return autoscaling_client.attach_instances(
        InstanceIds=[instance_id],
        AutoScalingGroupName=group_name
        )


list_instances()
print("\n")

instance = create_instance('test_intanceE')
instance_id = instance['Instances'][0]['InstanceId']
client.get_waiter('instance_running').wait(InstanceIds=[instance_id])

list_instances()

group_name = 'Proyecto2 ScalingGroup'
response = attach_instance(instance_id, group_name)
