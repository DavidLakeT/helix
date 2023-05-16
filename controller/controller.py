import boto3

# Especificar las credenciales de AWS
access_key = 'ASIA2JWTJAFB52TTTLET'
secret_key = 'mBXXGl+ZFy8Av2CJCBklasBbM8tOhESmY6syOWtV'
session_token = 'FwoGZXIvYXdzEBwaDONJHmCRDpN1RDcEASLIAXW1toY4ot3GD/R5+mDist67NhqJ/P/hR8OqYPKz0m5jA/Fuvy+HNdOkud2Vci0JmsFzHyWgKuHe40jefVzgSdCkDeQ9IJqa3a01TASm6DDAmgaAP3f/X9v4xKOxuSbobMMkaaAxTLYhOwtfM2/5imKjG6UBTwIM2l1VOXpseXihVR4TC5lcyr9h/lcvDNfv3yxy98s+rKnajoH6LvPYIb0m2DPH+k6aL3JP/dn9ZgG70vB/2QZXCzMEhAl8/117cXp6LebHVJxZKMyQj6MGMi2I9S1T4XYSZnoVXfFePy4EuScDvjUd2BNAWRYHqVMfNswcIVqCX8BbBWkeahA='
region = 'us-east-1'

# Crear una instancia del cliente EC2 con las credenciales especificadas
client = boto3.client(
    'ec2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    aws_session_token=session_token,
    region_name=region,
)
# Resto del código...

# Obtener todas las instancias EC2
response = client.describe_instances()

# Iterar sobre las reservas
for reservation in response['Reservations']:
    # Iterar sobre las instancias dentro de cada reserva
    for instance in reservation['Instances']:
        # Comprobar si la instancia tiene un nombre
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    # Imprimir el nombre de la instancia
                    print("Nombre de la instancia:", tag['Value'])
        else:
            print("Nombre de la instancia: (Sin nombre)")


'''instance = client.create_instances(
    ImageId='AMI_ID',  # Reemplaza con el ID de la imagen AMI que desees
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',  # Reemplaza con el tipo de instancia que desees
    KeyName='NOMBRE_PAR_LLAVES',  # Reemplaza con el nombre de tus llaves existentes
    SecurityGroupIds=['ID_DEL_GRUPO_DE_SEGURIDAD'],  # Reemplaza con el ID del grupo de seguridad que desees
    UserData='''#!/bin/bash
                # Incluye cualquier configuración adicional que desees ejecutar en la instancia al inicio
                echo "Configuración adicional"''',  # Reemplaza con los comandos de configuración adicionales que desees ejecutar
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{'Key': 'Name', 'Value': 'NOMBRE_DE_INSTANCIA'}]  # Reemplaza con el nombre que desees asignar a la instancia
    }]
)

print("Se creó la instancia con ID:", instance[0].id)'''



