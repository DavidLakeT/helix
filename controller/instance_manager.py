def list_instances(client, group_name):
    response = client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[group_name]
    )
    return response['AutoScalingGroups'][0]['Instances']


def create_instance(client, name):
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


def delete_instance(client, instance_id):
    return client.terminate_instances(InstanceIds=[instance_id])


def attach_instance(client, instance_id, group_name):
    return client.attach_instances(
        InstanceIds=[instance_id],
        AutoScalingGroupName=group_name
        )


def detach_instance(client, instance_id, group_name):
    return client.detach_instances(
        InstanceIds=[instance_id],
        AutoScalingGroupName=group_name,
        ShouldDecrementDesiredCapacity=True
        )
