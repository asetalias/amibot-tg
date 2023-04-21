import gen.amizone_pb2 as pb
import gen.amizone_pb2_grpc as pb_grpc
import grpc
from grpc import UnaryUnaryClientInterceptor
import base64

def cred_make():
    username = "8728670"
    password = "password"
    credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return credentials

def main():
    credentials = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel("amizone.fly.dev:443", credentials=credentials)
    stub = pb_grpc.AmizoneServiceStub(channel)
    cred = cred_make()
    metadata = [("authorization", f"Basic {cred}")]
    response = stub.GetAttendance(pb.EmptyMessage(), metadata=metadata)
    print(response)

if __name__ == "__main__":
    main()