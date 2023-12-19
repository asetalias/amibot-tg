import gen.amizone_pb2 as pb
from datetime import datetime
import logging

logger = logging.getLogger("AmiBot")


def exam_result_formatter(response: pb.ExamResultRecords, semester) -> str:
    logger.info("Formatting exam result")
    message = "Exam Results: \n\n"
    for sem in response.overall:
        if sem.semester.semester_ref == semester:
            message += f"SGPA: {sem.semester_grade_point_average:.2f}\n"
    message += (
        f"Current CGPA: {response.overall[-1].cumulative_grade_point_average:.2f}\n\n"
    )
    message += "Subject wise: \n"
    for subject in response.course_wise:
        message += f"{subject.course.code} \n"
        message += f"{subject.course.name} \n"
        message += f"Grade: {subject.score.grade} \n"
        message += f"Grade Point: {subject.score.grade_point} \n\n"

    return message


def get_wifi_info_formatter(response: pb.WifiMacInfo) -> str:
    logger.info("Formatting WiFi info")
    message = "WiFi Info: \n\nRegistered adresses:\n"
    for mac_address in response.addresses:
        message += f"→ {mac_address} \n"
    message += f"\nSlots: {response.slots} \n"
    message += f"Free slots: {response.free_slots}"
    return message


def get_attendance_formatter(response: pb.AttendanceRecords) -> str:
    logger.info("Formatting Attendance records")
    msg = "Attendance Records: \n\n"
    for record in response.records:
        percent = round(record.attendance.attended / record.attendance.held * 100, 2)
        msg += f"{record.course.code} \n"
        msg += f"{record.course.name} \n"
        msg += f" => {record.attendance.attended}/{record.attendance.held} ({percent})%  \n\n"
    return msg


def get_exam_formatter(response: pb.ExaminationSchedule) -> str:
    logger.info("Formatting exam schedule")
    msg = response.title + "\n\n"
    for exam in response.exams:
        date = datetime.fromtimestamp(exam.time.seconds)
        msg += f"{exam.course.code} \n"
        msg += f"{exam.course.name} \n"
        msg += f"{date.strftime('%d %b %Y')} \n"
        msg += f"{date.strftime('%H:%M')} \n"
        msg += f"{exam.mode} \n"
        try:
            msg += f"{exam.location} \n\n"
        except:
            msg += ""
    return msg


def get_courses_formatter(response: pb.Courses) -> str:
    logger.info("Formatting current courses")
    msg = "Current Courses: \n\n"
    for course in response.courses:
        link = f"<a href='{course.syllabus_doc}'>Syllabus</a>"
        msg += f"{course.ref.code} \n"
        msg += f"{course.ref.name} \n"
        msg += f"Marks : {course.internal_marks.have:.2f}/{course.internal_marks.max:.2f} \n"
        msg += f"{link} \n\n"
    return msg


def get_class_schedule_formatter(response: pb.ScheduledClasses) -> str:
    logger.info("Formatting class schedule")

    attendance_indicators = ""

    msg = "Class Schedule: \n\n"

    for index in response.classes:
        start = datetime.fromtimestamp(index.start_time.seconds)
        end = datetime.fromtimestamp(index.end_time.seconds)
        msg += f"{index.course.code} \n"
        msg += f"{index.course.name} \n"
        msg += f"{start.strftime('%H:%M')} to {end.strftime('%H:%M')} \n"
        msg += f"{index.faculty} \n"
        indicator = attendance_responder(index.attendance)
        msg += f"{index.room} \n" + f"Attendance : {indicator}"
        msg += "\n\n"
        attendance_indicators += indicator
    return attendance_indicators + "\n" + msg


def attendance_responder(val: pb.AttendanceState) -> str:
    if val == pb.PRESENT:
        return "🟢"

    if val == pb.ABSENT:
        return "🔴"

    if val == pb.PENDING:
        return "⚪️"

    else:
        return "🟡"


def peaker(classes) -> str:
    response = ""
    for item in classes:
        response += attendance_responder(item.attendance)
    return response
