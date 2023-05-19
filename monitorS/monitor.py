from grpc_client import grpc_service

# grpc_service("heartbeat")
print("cpu: " + str(grpc_service("metrics")))
