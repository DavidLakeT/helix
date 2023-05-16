import boto3
from datetime import datetime, timedelta

def list_instances(autoscaling_client):
    response = autoscaling_client.describe_auto_scaling_groups(AutoScalingGroupNames=[auto_scaling_group_name])

    if 'AutoScalingGroups' not in response or len(response['AutoScalingGroups']) == 0:
        print(f"No se encontró el Auto Scaling Group '{auto_scaling_group_name}'")
        return
    
    instances = response['AutoScalingGroups'] [0] ['Instances']

    return instances

def get_metrics(cloudwatch_client, instance_id):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10)

    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'cpu_usage',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': 'CPUUtilization',
                        'Dimensions': [
                            {
                                'Name': 'InstanceId',
                                'Value': instance_id
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Average',
                }
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )

    metric_results = response['MetricDataResults']
    return metric_results

if __name__ == "__main__":
    session = boto3.Session(region_name='us-east-1')
    autoscaling_client = session.client('autoscaling')
    cloudwatch_client = session.client('cloudwatch')

    auto_scaling_group_name = 'Proyecto2 ScalingGroup'
    instances = list_instances(autoscaling_client)

    if instances:
        for instance in instances:
            instance_id = instance['InstanceId']
            metrics = get_metrics(cloudwatch_client, instance_id)

            print(f"ID de instancia: {instance_id}")
            print(f"Estado: {instance['LifecycleState']}")

            if metrics:
                for metric_result in metrics:
                    metric_name = metric_result['Label']
                    values = metric_result['Values']
                    timestamps = metric_result['Timestamps']
                    for timestamp, value in zip(timestamps, values):
                        print(f'{metric_name} - Timestamp: {timestamp}, Value: {value}')
            else:
                print("No se encontraron métricas para la instancia.")

            print("---------")
    else:
        print(f"No se encontraron instancias en el Auto Scaling Group '{auto_scaling_group_name}'")