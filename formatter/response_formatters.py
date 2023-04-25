import gen.amizone_pb2 as pb
from datetime import datetime

def get_attendance_formatter(response: pb.AttendanceRecords) -> str:
    msg = "Attendance Records: \n\n"
    for record in response.records:
        percent = round(record.attendance.attended / record.attendance.held * 100, 2)
        msg += f"{record.course.code} \n"
        msg += f"{record.course.name} \n"
        msg += f" => {record.attendance.attended}/{record.attendance.held} ({percent})%  \n\n"
    return msg

def get_exam_formatter(response: pb.ExaminationSchedule()) -> str:
    print("Formatting")
    msg = response.title + "\n\n"
    for exam in response.exams:
        date = datetime.fromtimestamp(exam.time.seconds)
        msg += f"{exam.course.code} \n"
        msg += f"{exam.course.name} \n"
        msg += f"{date.strftime('%d %b %Y')} \n\n"
    return msg
        