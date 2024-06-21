from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime
from django.core.serializers import serialize
from users.models import SimpleRecord, User
import json


def backstageindex(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    if request.session.get('identity') not in ['管理员', '系统管理员']:
        return redirect(reverse('index'))
    else:
        current_date = datetime.now().strftime("%Y-%m-%d")
        username = request.session.get('username', 'Guest')
        message = {
            'current_date': current_date,
            'username': username,
        }
    return render(request, 'backstage.html', message)


def recent_record(request):
    # 获取最近的12条查询记录，按时间倒序排列
    recent_records = SimpleRecord.objects.order_by('-timestamp')[:12]
    records_data = []
    for record in recent_records:
        records_data.append({
            'timestamp': record.timestamp,
            'username': record.name,
            'type': record.record_type
        })

    return JsonResponse(records_data, safe=False)


def count(request):
    usernum = User.objects.count()
    predictionnum = SimpleRecord.objects.count()
    message = {'usernum': usernum,
               'predictionnum': predictionnum
               }
    return JsonResponse(message, safe=False)


def searchuser(request):
    word = request.GET.get('searchword', '')
    records = User.objects.filter(name__icontains=word)
    data = []
    for record in records:
        data.append({
            'timestamp': record.timestamp.strftime('%Y{y}%m{m}%d{d}%H{H}%M{M}%S{S}').format(y='年', m='月', d='日',
                                                                                            H='时', M='分', S='秒'),
            'email': record.email,
            'sex': record.sex,
            'username': record.name,
        })
    return JsonResponse(data, safe=False)


def detailuser(request):
    username = request.GET.get('username', '')
    records = SimpleRecord.objects.filter(name=username).order_by('-timestamp')
    records = serialize('json', records)
    records_data = json.loads(records)
    records = [record['fields'] for record in records_data]
    # print(records)
    return JsonResponse(records, safe=False)
