import base64
import grpc
import gen.amizone_pb2_grpc as pb_grpc

def cred_maker(username, password):
    credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    metadata = [("authorization", f"Basic {credentials}")]
    return metadata

def stubber(username, password):
    metadata = cred_maker(username, password)
    credentials = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel("amizone.fly.dev:443", credentials=credentials)
    stub = pb_grpc.AmizoneServiceStub(channel)
    return stub


