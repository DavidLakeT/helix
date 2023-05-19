import random
import grpc
from concurrent import futures
from protos import monitor_pb2
from protos import monitor_pb2_grpc


def heartbeat(stub):
    response = stub.Heartbeat(monitor_pb2.HeartbeatRequest())
    return response.status


def instance_metrics(stub):
    response = stub.InstanceMetrics(
            monitor_pb2.InstanceMetricsRequest())
    return response.cpu_load


def grpc_service(req):
    with grpc.insecure_channel('[::1]') as channel:
        stub = monitor_pb2_grpc.MonitorServiceStub(channel)

        if req == "heartbeat":
            return heartbeat(stub)

        return instance_metrics(stub)
