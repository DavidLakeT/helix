def create_instance(client):
    instance = client.run_instances(
        MinCount=1,
        MaxCount=1,
        ImageId='ami-060a2d7b6dd28b169',
        InstanceType='t2.micro',
        KeyName='vockey',
        SecurityGroupIds=['default'],
        UserData='',
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': ''}]
        }])
    instance_id = instance['Instances'][0]['InstanceId']
    client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
    return instance_id


def terminate_instance(client, instance_id):
    return client.terminate_instances(InstanceIds=[instance_id])


def cleaner(ec2_client):
    description = ec2_client.describe_instances()
    for reservation in description['Reservations']:
        for instance in reservation['Instances']:
            terminate_instance(ec2_client, instance['InstanceId'])


def instance_setup(ec2_client):
    id1 = create_instance(ec2_client)
    id2 = create_instance(ec2_client)
    return (id1, id2)
