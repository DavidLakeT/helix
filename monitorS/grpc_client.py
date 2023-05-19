import json
import grpc
from monitorS import monitor_service_pb2
from monitorS import monitor_service_pb2_grpc


def heartbeat(stub):
    response = stub.HeartBeat(monitor_service_pb2.HeartBeatRequest())
    return response.status


def instance_metrics(stub):
    response = stub.InstanceMetrics(
            monitor_service_pb2.InstanceMetricsRequest())
    return response.cpu_load


def grpc_service(req):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = monitor_service_pb2_grpc.MonitorServiceStub(channel)
        smg = json.loads(req)
        serv = smg["service"]

        if serv == "heartbeat":
            return heartbeat(stub)

        return instance_metrics(stub)
