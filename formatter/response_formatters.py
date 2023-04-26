import gen.amizone_pb2 as pb
from datetime import datetime
import logging

logger = logging.getLogger()

def get_attendance_formatter(response: pb.AttendanceRecords) -> str:
    logger.info("Formatting")
    msg = "Attendance Records: \n\n"
    for record in response.records:
        percent = round(record.attendance.attended / record.attendance.held * 100, 2)
        msg += f"{record.course.code} \n"
        msg += f"{record.course.name} \n"
        msg += f" => {record.attendance.attended}/{record.attendance.held} ({percent})%  \n\n"
    return msg

def get_exam_formatter(response: pb.ExaminationSchedule) -> str:
    logger.info("Formatting")
    msg = response.title + "\n\n"
    for exam in response.exams:
        date = datetime.fromtimestamp(exam.time.seconds)
        msg += f"{exam.course.code} \n"
        msg += f"{exam.course.name} \n"
        msg += f"{date.strftime('%d %b %Y')} \n\n"
    return msg
        
def get_courses_formatter(response: pb.Courses) -> str:
    logger.info("Formatting")
    msg = "Current Courses: \n\n"
    for course in response.courses:
        link = f"<a href='{course.syllabus_doc}'>Syllabus</a>"
        msg += f"{course.ref.code} \n"
        msg += f"{course.ref.name} \n"
        msg += f"Marks : {course.internal_marks.have}/{course.internal_marks.max} \n"
        msg += f"{link} \n\n"
    return msg

def get_class_schedule_formatter(response: pb.ScheduledClasses) -> str:
    logger.info("Formatting")
    msg = "Class Schedule: \n\n"
    for index in response.classes:
        start = datetime.fromtimestamp(index.start_time.seconds)
        end = datetime.fromtimestamp(index.end_time.seconds)
        msg += f"{index.course.code} \n"
        msg += f"{index.course.name} \n"
        msg += f"{start.strftime('%H:%M')} to {end.strftime('%H:%M')} \n"
        msg += f"{index.faculty} \n"
        msg += f"{index.room} \n" + f"Attendance : {attendance_responder(index.attendance)}"
        msg += "\n\n"
    return msg

def attendance_responder(val: pb.AttendanceState) -> str:
    if val == pb.PRESENT:
        return "🟢"

    if val == pb.ABSENT:
        return "🔴"

    if val == pb.PENDING:
        return "⚪️"
    
    else:
        return "🟡"