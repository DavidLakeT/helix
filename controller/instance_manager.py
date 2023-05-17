def list_instances(client):
    response = client.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        print("Nombre de la instancia:", tag['Value'])
            else:
                print("Nombre de la instancia: (Sin nombre)")


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
