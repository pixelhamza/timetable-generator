from django.db import models

from django.db import models

class Course(models.Model):
    COURSE_TYPES = [
        ("Core", "Core"),
        ("Elective", "Elective"),
        ("Lab", "Lab"),
        ("Skill", "Skill-Based"),
    ]
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=100)
    credits = models.IntegerField()
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES)
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Faculty(models.Model):
    faculty_id = models.CharField(max_length=10, unique=True)
    faculty_name = models.CharField(max_length=100)
    availability = models.JSONField(default=dict)  

    def __str__(self):
        return self.faculty_name


class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    student_name = models.CharField(max_length=100)
    elective_choices = models.JSONField(default=list)  

    def __str__(self):
        return self.student_name


class Room(models.Model):
    ROOM_TYPES = [
        ("Lecture", "Lecture"),
        ("Lab", "Lab"),
    ]
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)

    def __str__(self):
        return self.room_number


class TimeSlot(models.Model):
    DAYS = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
    ]
    day = models.CharField(max_length=3, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} {self.start_time}-{self.end_time}"


class TimetableEntry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    student_group = models.CharField(max_length=50, default="All")

    def __str__(self):
        return f"{self.course.course_code} - {self.timeslot}"

