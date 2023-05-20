# helix
### info de la materia: ST0263
### Estudiante(s): 
-  David Jose Cardona Nieves, djcardonan@eafit.edu.co;
-  Juan David Valencia Torres, jdvalencit@eafit.edu.co; 
-  Tomas Atehortua Ceferino, tatehortuc@eafit.edu.co; 
-  Daniel Arango Hoyos, darangoh@eafit.edu.co
### Profesor: 
-  Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# 1. breve descripción de la actividad

El objetivo del proyecto es desarrollar un servicio de autoescalamiento que permita gestionar automáticamente la cantidad de instancias EC2 en Amazon Web Services, en función de la carga y la vivacidad de las aplicaciones en ejecución. Para esto el sistema debe ser capaz de monitorear el estado y la carga de las instancias de aplicación, tomar decisiones basadas en esta información y ejecutar acciones como la creación o destrucción de instancias según las políticas establecidas. 

El propósito es optimizar el uso de recursos y garantizar un rendimiento adecuado de las aplicaciones, escalando automáticamente el número de instancias de acuerdo con la demanda y la carga del sistema. 

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- Diseño e implementación de un proceso principal de monitoreo (MonitorS) que consulta periódicamente el estado y la carga de las instancias de aplicación (AppInstance).
- Comunicación entre MonitorS y MonitorC a través de gRPC.
- Desarrollo de un ControllerASG que se ejecuta en la misma instancia del MonitorS y tiene acceso a la información recolectada.
- Uso del SDK de la nube para ejecutar funciones de infraestructura como código, permitiendo la creación, modificación y borrado de instancias EC2.
- Configuración de una instancia EC2 con el software base, la AppInstance y el agente MonitorC, y creación de una imagen AMI personalizada para la creación de nuevas instancias.
- Establecimiento de políticas de creación y destrucción de instancias basadas en la carga y la demanda del sistema.


# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

![image](https://github.com/jdvalencit/helix/assets/61467004/6929cebb-c2cd-43e4-ab43-c4b5ddd77ee3)
 
La estructura del proyecto se compone de 4 componentes clave: 
- __MonitorS__: Es el proceso principal de monitoreo. Se encarga de consultar periódicamente el estado y la carga de las instancias de aplicación (AppInstance). Utiliza gRPC para comunicarse con MonitorC y obtener información relevante.

- __MonitorC__: Es un proceso que se ejecuta en cada instancia de AppInstance y ofrece varios servicios mediante una API hacia MonitorS. Algunos de los servicios implementados en MonitorC incluyen el Ping/Pong o Heartbeat para detectar la vivacidad de la instancia, GetMetrics para obtener métricas de carga, Registro y Desregistro del MonitorS, entre otros.

- __ControllerASG__: Es un proceso o aplicación que se ejecuta en la misma instancia que MonitorS. Tiene acceso a la información recolectada por MonitorS a través de memoria compartida. Utiliza el SDK de la nube para ejecutar funciones de Infraestructura como Código y realizar operaciones en los servicios de la nube. Su función principal es administrar la creación, modificación y destrucción de instancias EC2 basadas en la carga y la demanda del sistema.

- __SDK de la nube__: Se utiliza para interactuar con los servicios de la nube, en este caso, principalmente con el servicio de gestión de instancias EC2. Permite al ControllerASG realizar operaciones de infraestructura como código, como la creación y eliminación de instancias.

La interacción entre estos componentes se realiza a través de gRPC, que proporciona una comunicación eficiente y confiable entre MonitorS y MonitorC. MonitorS consulta periódicamente el estado de las instancias y recopila métricas relevantes, mientras que ControllerASG utiliza esta información para tomar decisiones de escalado, creando o eliminando instancias según sea las políticas indicadas, que en nuestro caso se rige por el uso de CPU en las instancias.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

## como se compila y ejecuta.
Para poder ejecutar el proyecto primero es necesario tener instalado Python e instalar las siguientes dependencias:
```
boto3==1.26.137
grpcio==1.54.2
grpcio-tools==1.54.2
python-dotenv==1.0.0
```
Seguido de esto, cree un archivo .env en la carpeta ROOT del proyecto, en el que tendrá que declarar lo siguiente:
```
AWS_ACCESS_KEY=<ingresar_la_aws_access_key_de_su_CLI>
AWS_SECRET_KEY=<ingresar_la_aws_secret_key_de_su_CLI>
AWS_SESSION_TOKEN=<ingresar_el_aws_session_token_de_su_CLI>
REGION=<region_en_donde_alojara_sus_instancias>
CPU_LOWER_LIMIT=<minimo_uso_de_CPU(ex:0.25;0.3)>
CPU_UPPER_LIMIT=<maximo_uso_de_CPU(ex:0.7;0.8)>
MIN_INSTANCES=<minimas_instancias_a_crear(ex:2;3)>
MAX_INSTANCES=<maximas_instancias_a_crear(ex:5;7)>
```
Con estas variables de entorno ya configuradas, lo único que necesita es el Image Id de un AMI para poder instanciar las máquinas en AWS, una vez conseguido diríjase al archivo `instance_manager.py` y cambie la siguiente variable por su Image Id:
```
ImageId='image_id',
```
Ya con todo configurado, proceda a correr `monitor_c.py`:
```
python3 monitorC/monitor_c.py
```
Y por último, ejecute `controller.py` en una nueva:
```
python3 controller/controller.py
```
Y ya podrá ver cómo se crean o se eliminan instancias a partir de una simulación de uso de la CPU.

## detalles técnicos
## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
Para configurar los valores con los que se va a ejecutar el proyecto se utiliza un archivo de configuración .env en la carpeta root del proyecto. Cuenta con la siguiente estructura:
```
AWS_ACCESS_KEY=<ingresar_la_aws_access_key_de_su_CLI>
AWS_SECRET_KEY=<ingresar_la_aws_secret_key_de_su_CLI>
AWS_SESSION_TOKEN=<ingresar_el_aws_session_token_de_su_CLI>
REGION=<region_en_donde_alojara_sus_instancias>
CPU_LOWER_LIMIT=<minimo_uso_de_CPU(ex:0.25;0.3)>
CPU_UPPER_LIMIT=<maximo_uso_de_CPU(ex:0.7;0.8)>
MIN_INSTANCES=<minimas_instancias_a_crear(ex:2;3)>
MAX_INSTANCES=<maximas_instancias_a_crear(ex:5;7)>
```

## detalles de la organización del código por carpetas o descripción de algún archivo.
```
├── controller
│   ├── controller.py
│   ├── instance_manager.py
│   ├── monitorS
│   │   ├── grpc_client.py
│   │   └── __pycache__
│   │       └── grpc_client.cpython-310.pyc
│   ├── protos
│   │   ├── monitor_pb2_grpc.py
│   │   ├── monitor_pb2.py
│   │   ├── monitor.proto
│   │   └── __pycache__
│   │       ├── monitor_pb2.cpython-310.pyc
│   │       └── monitor_pb2_grpc.cpython-310.pyc
│   └── __pycache__
│       └── instance_manager.cpython-310.pyc
├── LICENSE
├── monitorC
│   ├── monitor_c.py
│   └── protos
│       ├── monitor_pb2_grpc.py
│       ├── monitor_pb2.py
│       ├── monitor.proto
│       └── __pycache__
│           ├── monitor_pb2.cpython-310.pyc
│           └── monitor_pb2_grpc.cpython-310.pyc
└── README.md

```


## 
## opcionalmente - si quiere mostrar resultados o pantallazos 


# 4. otra información que considere relevante para esta actividad.

# referencias:

- https://grpc.io
- https://docs.aws.amazon.com
- https://www.python.org

#### versión README.md -> 1.0 (2022-agosto)

