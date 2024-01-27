# linktracker/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import VisitedLink
from datetime import datetime
from django.db.models import Q

@csrf_exempt
def visited_links(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            links = data.get('links', [])
            for link in links:
                VisitedLink.objects.create(link=link)
            return JsonResponse({'status': 'ok'}, status=200)
        except Exception as e:
            return JsonResponse({'status': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'Method Not Allowed! Use POST method'}, status=405)

@csrf_exempt
def visited_domains(request):
    if request.method == 'GET':
        try:
            from_time = request.GET.get('from')
            to_time = request.GET.get('to')

            # Формируем фильтр, если from_time и/или to_time заданы
            filter_params = Q()
            if from_time:
                filter_params &= Q(visited_at__gte=datetime.fromtimestamp(int(from_time)))
            if to_time:
                filter_params &= Q(visited_at__lte=datetime.fromtimestamp(int(to_time)))

            domains = (
                VisitedLink.objects.filter(filter_params)
                .values_list('link', flat=True)
                .distinct()
            )
            domain_list = list({VisitedLink(link=domain).get_domain() for domain in domains})
            return JsonResponse({'domains': domain_list, 'status': 'ok'}, status=200)
        except Exception as e:
            return JsonResponse({'status': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'Method Not Allowed! Use GET method'}, status=405)
