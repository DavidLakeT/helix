import random
import time
import grpc
import os
import json
from protos import monitor_pb2
from protos import monitor_pb2_grpc
from concurrent import futures


class MonitorServiceServicer(monitor_pb2_grpc.MonitorServiceServicer):
    def Heartbeat(self, request, context):
        print("heartbeat")
        return monitor_pb2.HeartbeatOkResponse(status=True)

    def InstanceMetrics(self, request, context):
        print("metrics")
        return monitor_pb2.InstanceMetricsOkResponse(cpu_load=0.5)


def main():
    print("Monitor C:")
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=4))
    monitor_pb2_grpc.add_MonitorServiceServicer_to_server(
        MonitorServiceServicer(), server)

    server.add_insecure_port("[::1]")
    server.start()
    server.wait_for_termination()


'''
def main():
    while True:
        print("\n------------------------------------\n" +
              "\nCPU: \n")
        cpu_usage = random.random()
        print(cpu_usage)
        time.sleep(1)
        '''


if __name__ == "__main__":
    main()
