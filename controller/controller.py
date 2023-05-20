from instance_manager import create_instance, terminate_instance, cleaner, instance_setup
from dotenv import load_dotenv
from monitorS import grpc_client
import time
import os
import boto3

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
cpu_direction = "up"
cpu_avg = 0.5

ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    aws_session_token=session_token,
    region_name=region,
)

print("Deleting all previous instances\n")
cleaner(ec2_client)
print("Creating initial instances")

id1, id2 = instance_setup(ec2_client)
instance_list.append(id1)
instance_list.append(id2)

current_instances = 2
while True:
    cpu_avg = grpc_client.grpc_service("metrics", cpu_avg, cpu_direction)
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

    if cpu_avg > 0.75:
        cpu_direction = "down"
    elif cpu_avg < 0.25:
        cpu_direction = "up"

    print("-------------------------------------------------")
    time.sleep(10)

'''

Usted está generando constantemente números en MonitorC.
Esos números se generan a partir de un random que se crea la primera vez. (0.0 a 1.0)

En el MonitorC usted tiene una variable global (dirección), esa dirección por default
es nula (None). Si usted recibe un rpc "setDirection" que tiene las posibles opciones
"up", "down" y "none", cuando lo recibe usted actualiza la dirección global (que va a
ser la que va a utilizar luego en la función GetNumber, por lo que debe eliminar el
parámetro que tiene actualmente esa función para dirección).

Entonces el Controller sigue recibiendo los números que el MonitorC le está pasando
(que ya cambiaron de dirección), así ya todos los siguientes serán en una dirección y
no tiene que estar pidiendo la dirección en cada request y es más fácil testear.
Eso por la parte del MonitorC. 

--------

Cuando cree una instancia, usted llama al método que tenga para listar las instancias
y si puede obtenga la fecha de creación, de forma que pueda ver cuál fué la más reciente.

'''