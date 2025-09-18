
from rest_framework import serializers


class LunchBreakSerializer(serializers.Serializer):
    start = serializers.TimeField()
    end = serializers.TimeField()

class ConfigSerializer(serializers.Serializer):
    workingDays = serializers.ListField(child=serializers.CharField())
    startTime = serializers.TimeField()
    endTime = serializers.TimeField()
    slotDuration = serializers.IntegerField()
    lunchBreak = LunchBreakSerializer()
    algorithm = serializers.CharField() 

class CourseSerializer(serializers.Serializer):

    Course_ID = serializers.CharField(max_length=100)
    Course_Name = serializers.CharField(max_length=100)
    Type = serializers.CharField(max_length=50)
    Weekly_Hours = serializers.CharField(max_length=10)
    Department = serializers.CharField(max_length=100)

class FacultySerializer(serializers.Serializer):
    Faculty_ID = serializers.CharField(max_length=100)
    Faculty_Name = serializers.CharField(max_length=100)
    Department = serializers.CharField(max_length=100)

class RoomSerializer(serializers.Serializer):
    Room_ID = serializers.CharField(max_length=100)
    Room_Type = serializers.CharField(max_length=50)
    Capacity = serializers.CharField(max_length=10)

class RequestDataSerializer(serializers.Serializer):
    courses = CourseSerializer(many=True)
    faculty = FacultySerializer(many=True)
    rooms = RoomSerializer(many=True)

class TimetableRequestSerializer(serializers.Serializer):
    config = ConfigSerializer()
    data = RequestDataSerializer()