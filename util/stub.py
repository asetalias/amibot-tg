import grpc
import base64
import gen.amizone_pb2_grpc as pb_grpc

def basic_cred():
    username = "8728670"
    password = "password"
    credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return credentials

cred = basic_cred()
metadata = [("authorization", f"Basic {cred}")]

credentials = grpc.ssl_channel_credentials()
channel = grpc.secure_channel("amizone.fly.dev:443", credentials=credentials)
stub = pb_grpc.AmizoneServiceStub(channel)

