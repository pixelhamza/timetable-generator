from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import pandas as pd
from .models import Course, Faculty, Student, Room, TimeSlot
def home(request):
    return HttpResponse("BaseApp API is working!")

@api_view(['POST'])
def upload_data(request):
    try:
        # --- Handle Course CSV ---
        if 'courses' in request.FILES:
            courses_df = pd.read_csv(request.FILES['courses'])
            for _, row in courses_df.iterrows():
                Course.objects.update_or_create(
                    course_code=row['course_code'],
                    defaults={
                        "course_name": row['course_name'],
                        "credits": row['credits'],
                        "course_type": row['course_type'],
                        "department": row['department']
                    }
                )

        # --- Handle Faculty CSV ---
        if 'faculty' in request.FILES:
            faculty_df = pd.read_csv(request.FILES['faculty'])
            for _, row in faculty_df.iterrows():
                Faculty.objects.update_or_create(
                    faculty_id=row['faculty_id'],
                    defaults={
                        "faculty_name": row['faculty_name'],
                        "availability": eval(row['availability'])  # expect JSON-like string
                    }
                )

        # --- Handle Students CSV ---
        if 'students' in request.FILES:
            students_df = pd.read_csv(request.FILES['students'])
            for _, row in students_df.iterrows():
                Student.objects.update_or_create(
                    student_id=row['student_id'],
                    defaults={
                        "student_name": row['student_name'],
                        "elective_choices": eval(row['elective_choices'])
                    }
                )

        return Response({"message": "Data uploaded successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

