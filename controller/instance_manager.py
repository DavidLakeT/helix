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


def terminate_instance(client, instance_id):
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


def new_instance(ec2_client, autoscaling_client, name, group_name):
    instance = create_instance(ec2_client, name)
    instance_id = instance['Instances'][0]['InstanceId']
    ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
    at_response = attach_instance(autoscaling_client, instance_id, group_name)
    return (instance_id, at_response)


def delete_instance(ec2_client, autoscaling_client, instance_id, group_name):
    dt_response = detach_instance(autoscaling_client, instance_id, group_name)
    terminate = terminate_instance(ec2_client, instance_id)
    return (dt_response, terminate)


def cleaner(ec2_client, autoscaling_client, group_name):
    instances = list_instances(autoscaling_client, group_name)
    for instance in instances:
        delete_instance(ec2_client, autoscaling_client, instance['InstanceId'], group_name)


def instance_setup(ec2_client, autoscaling_client, group_name):
    id1, _ = new_instance(ec2_client, autoscaling_client, '', group_name)
    id2, _ = new_instance(ec2_client, autoscaling_client, '', group_name)
    return (id1, id2)
