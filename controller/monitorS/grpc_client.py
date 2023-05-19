import grpc
from protos import monitor_pb2
from protos import monitor_pb2_grpc


def heartbeat(stub):
    response = stub.Heartbeat(monitor_pb2.HeartbeatRequest())
    return response.status


def instance_metrics(stub, nprev, dir):
    response = stub.InstanceMetrics(
            monitor_pb2.InstanceMetricsRequest(prev=nprev, direction=dir))
    return response.cpu_load


def grpc_service(req, prev=None, direction=None, ips=None):
    with grpc.insecure_channel('[::1]') as channel:
        stub = monitor_pb2_grpc.MonitorServiceStub(channel)

        if req == "heartbeat":
            return heartbeat(stub)

        return instance_metrics(stub, prev, direction)
