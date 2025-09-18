
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, time, timedelta

from .serializers import TimetableRequestSerializer
from .logic.solver import Timetable


def run_solver_and_adapt_output(validated_data):
    config = validated_data['config']
    data = validated_data['data']

  
    time_slots = []
    lunch_start = config['lunchBreak']['start']
    lunch_end = config['lunchBreak']['end']
    
    for day in config['workingDays']:
    
        start_dt = datetime.combine(datetime.today(), config['startTime'])
        end_dt = datetime.combine(datetime.today(), config['endTime'])
        current_dt = start_dt
        
        while current_dt < end_dt:
            slot_end_dt = current_dt + timedelta(minutes=config['slotDuration'])
            
            
            is_in_lunch = not (current_dt.time() >= lunch_end or slot_end_dt.time() <= lunch_start)

            if not is_in_lunch:
                time_str = f"{current_dt.strftime('%H:%M')}-{slot_end_dt.strftime('%H:%M')}"
                time_slots.append({'day': day, 'time': time_str})
            
            current_dt = slot_end_dt

    num_days = len(config['workingDays'])
    hours_per_day = len(time_slots) // num_days if num_days > 0 else 0
    timetable = Timetable(days=num_days, hours_per_day=hours_per_day)

    for course_data in data['courses']:
        timetable.add_course(course_data['Course_ID'], course_data['Course_Name'], int(course_data['Weekly_Hours']))
    for faculty_data in data['faculty']:
        timetable.add_teacher(faculty_data['Faculty_ID'], faculty_data['Faculty_Name'])
    for room_data in data['rooms']:
        timetable.add_room(room_data['Room_ID'], room_data['Room_Type'])

    generated_schedule = timetable.generate()


    assignments = {}
    day_map = {day: i for i, day in enumerate(config['workingDays'])}
    
    for entry in generated_schedule:
        day_index = entry['day']
        hour_index = entry['hour']
        
    
        slot_index_in_day = day_index * hours_per_day + hour_index
        if slot_index_in_day < len(time_slots):
            slot = time_slots[slot_index_in_day]
            slot_key = f"{slot['day'].capitalize()}-{slot['time']}"
            
            course_info = next((c for c in data['courses'] if c['Course_ID'] == entry['course_id']), {})
            faculty_info = next((f for f in data['faculty'] if f['Faculty_ID'] == entry['teacher_id']), {})
            room_info = next((r for r in data['rooms'] if r['Room_ID'] == entry['room_id']), {})

            assignments[slot_key] = {
                "course": course_info, "faculty": faculty_info, "room": room_info
            }
    
 
    final_result = {
        "assignments": assignments, "conflicts": [],
        "stats": {
            "totalClasses": len(data['courses']),
            "scheduledClasses": len(generated_schedule),
            "conflicts": 0,
        }
    }
    
    return final_result

class TimetableGeneratorView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TimetableRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            timetable_result = run_solver_and_adapt_output(serializer.validated_data)
            return Response(timetable_result, status=status.HTTP_200_OK)
        except Exception as e:

            return Response(
                {"error": "An error occurred during timetable generation.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )