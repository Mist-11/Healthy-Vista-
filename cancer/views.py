from cancer.usemodel import *
from tool import draw_BC
from cancer import new_columns, record_columns
from report import *
import os
from tool import danger
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime
import json
from users.models import SimpleRecord
import numpy as np


def BCindex(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    else:
        current_date = datetime.now().strftime("%Y-%m-%d")
        username = request.session.get('username', 'Guest')
        message = {
            'current_date': current_date,
            'username': username,
        }
    return render(request, 'Breastcancer.html', message)


# 使用预测
def BCpre(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    else:
        parameters = json.loads(request.body.decode('utf-8'))
        # 创建空的DataFrame
        df = pd.DataFrame()
        # 遍历字典，添加数据到DataFrame
        for key, value in parameters.items():
            if isinstance(value, list):  # 如果值是列表
                for i, val in enumerate(value):
                    df[f'{key}_{i}'] = [val]  # 以键的名称和序号作为列名
            else:  # 如果值不是列表
                df[key] = [value]  # 直接添加到DataFrame
        df.columns = new_columns
        if df.shape[1] != 79:
            return JsonResponse({"message": "请完整输入所有参数。"}, status=400)
        else:
            # 获取参数
            user = request.session.get('username', 'Guest')
            sex = request.session.get('sex', 'unknown')
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d%H%M%S")
            # 预测
            surv = usedeephit(df)
            surv = surv.round(5)
            time_point = danger(surv)
            image_path = draw_BC(surv, user, formatted_time)  # 绘图
            pdf_path = BC_Report(image_path, parameters, user, sex, formatted_time, time_point)  # 生成报告
            os.remove(image_path)
            surv.index = surv.index.astype(int)
            surv = surv.to_json(orient='split')
            df.columns = record_columns
            current_time = current_time.timestamp() * 1000
            SimpleRecord.pre_record(user, "乳腺癌", current_time, pdf_path)
            return JsonResponse(surv, safe=False)


def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def HDindex(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    else:
        current_date = datetime.now().strftime("%Y-%m-%d")
        username = request.session.get('username', 'Guest')
        message = {
            'current_date': current_date,
            'username': username,
        }
    return render(request, 'Heartdisease.html', message)


def HDpre(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    else:
        data = json.loads(request.body.decode('utf-8'))
        df = pd.DataFrame([data])
        # print(df)
        df = df.replace('', np.nan)
        if df.isnull().any().any():
            return JsonResponse({"message": "请完整输入所有参数。"}, status=400)
        else:
            try:
                df.astype(float)
            except ValueError:
                return JsonResponse({"message": "请输入数字。"}, status=400)
            # 获取参数
            user = request.session.get('username', 'Guest')
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d%H%M%S")
            # 预测
            surv = uselightgbm(df)
            pdf_path = HD_Report(surv, data, user, formatted_time)  # 生成报告
            current_time = current_time.timestamp() * 1000
            SimpleRecord.pre_record(user, "心脏病", current_time, pdf_path)  # 记录
            return JsonResponse({'result': int(surv[0])})


def HEindex(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    else:
        current_date = datetime.now().strftime("%Y-%m-%d")
        username = request.session.get('username', 'Guest')
        message = {
            'current_date': current_date,
            'username': username,
        }
    return render(request, 'Hepatitis.html', message)


def HEpre(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('login'))
    else:
        data = json.loads(request.body.decode('utf-8'))
        df = pd.DataFrame([data])
        df = df.replace('', np.nan)
        if df.isnull().any().any():
            return JsonResponse({"message": "请完整输入所有参数。"})
        else:
            try:
                df1 = df.astype(float)
            except ValueError:
                return JsonResponse({"message": "请输入数字。"})
            # 获取参数
            user = request.session.get('username', 'Guest')
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d%H%M%S")
            # 预测
            surv = userandomforest(df)
            # print(surv)
            pdf_path = HE_report(surv, data, user, formatted_time)  # 生成报告
            current_time = current_time.timestamp() * 1000
            SimpleRecord.pre_record(user, "肝炎", current_time, pdf_path)  # 记录
            return JsonResponse({'result': int(surv[0])})
