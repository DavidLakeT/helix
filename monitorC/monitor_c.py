import random
import grpc
from concurrent import futures
from protos import monitor_pb2
from protos import monitor_pb2_grpc


class MonitorServiceServicer(monitor_pb2_grpc.MonitorServiceServicer):
    def Heartbeat(self, request, context):
        return monitor_pb2.HeartbeatOkResponse(status=True)

    def InstanceMetrics(self, request, context):
        cpu_value = get_number(prev=request.prev, direction=request.direction)
        return monitor_pb2.InstanceMetricsOkResponse(cpu_load=cpu_value)


def main():
    print("Monitor C:")
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=4))
    monitor_pb2_grpc.add_MonitorServiceServicer_to_server(
        MonitorServiceServicer(), server)

    server.add_insecure_port("[::1]")
    server.start()
    server.wait_for_termination()


def get_number(prev=None, direction=None, range=0.1):
    if prev is None:
        cpu_usage = random.random()
        return cpu_usage
    else:
        if direction is None:
            lower_limit = prev - range
            upper_limit = prev + range

            cpu_usage = random.uniform(lower_limit, upper_limit)
            return cpu_usage
        elif direction == "down":
            lower_limit = prev
            upper_limit = prev - range

            cpu_usage = random.uniform(lower_limit, upper_limit)
            return cpu_usage
        elif direction == "up":
            lower_limit = prev
            upper_limit = prev + range

            cpu_usage = random.uniform(lower_limit, upper_limit)
            return cpu_usage


if __name__ == "__main__":
    main()
