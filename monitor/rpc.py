import grpc
from concurrent import futures
import time

from monitor.aws import get_metrics

instance_id = ""

class MonitorService(monitor_pb2_grpc.MonitorServiceServicer):
    def Heartbeat(self, request, context):
        response = monitor_pb2.HeartbeatOkResponse()
        return response
    
    def InstanceMetrics(self, request, context):
        global instance_id
        instance_id = "aca_va_el_id"
        metrics = get_metrics(instance_id)

        response = monitor_pb2.InstanceMetricsOkResponse()
        response.cpu_load = metrics('cpu_load')

        return response
    
def serveRpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    monitor_pb2_grpc.add_MonitorServiceServicer_to_server(MonitorService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serveRpc()