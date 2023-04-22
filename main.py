import gen.amizone_pb2 as pb
from util.stub import stub, metadata


def main():
    response = stub.GetAttendance(pb.EmptyMessage(), metadata=metadata)
    print(response.records[0].attendance)

if __name__ == "__main__":
    main()