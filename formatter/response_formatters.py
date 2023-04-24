import gen.amizone_pb2 as pb

def get_attendance_formatter(response: pb.AttendanceRecords) -> str:
    msg = "Attendance Records: \n\n"
    for record in response.records:
        percent = round(record.attendance.attended / record.attendance.held * 100, 2)
        msg += f"{record.course.code} \n"
        msg += f"{record.course.name} \n"
        msg += f" => {record.attendance.attended}/{record.attendance.held} ({percent})%  \n\n"
    return msg