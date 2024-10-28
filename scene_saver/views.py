from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

from scene_saver.models import ScaneSaverInfo


@csrf_exempt
def save_scene(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            save_time = data.get('save_time')
            file_path = data.get('file_path')

            if not all([username, save_time, file_path]):
                return JsonResponse({"status": "error", "message": "Missing data in request"}, status=400)

            save_time = timezone.make_aware(datetime.fromisoformat(save_time))
            scene_save = ScaneSaverInfo(username=username, save_time=save_time, file_path=file_path)
            scene_save.save()

            print(f"Received data: Username: {username}, Save Time: {save_time}, File Path: {file_path}")

            return JsonResponse({"status": "success", "message": "Data received successfully!"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)


@staff_member_required
def scene_save_list(request):
    saves = ScaneSaverInfo.objects.all()
    return render(request, 'scene_save_info/scene_save_list.html', {'saves': saves})
