import gen.amizone_pb2 as pb
import gen.amizone_pb2_grpc as pb_grpc
import grpc
from grpc import UnaryUnaryClientInterceptor
import base64

def authentication() -> UnaryUnaryClientInterceptor:
    username = "8728670"
    password = "password"
    credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
    metadata = UnaryUnaryClientInterceptor()
    return metadata

def main():
    channel = grpc.insecure_channel("amizone.fly.dev:443")
    intercept_channel = grpc.intercept_channel(channel, authentication())
    stub = pb_grpc.AmizoneServiceStub(intercept_channel)
    response = stub.GetAttendance(pb.EmptyMessage())
    print(response)

if __name__ == "__main__":
    main()