# Create your views here.

import time,datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from frontend.models import UserLog, IPLog

def bw_report_users(request):
    userloglist_qs = UserLog.objects.filter(date=datetime.datetime.utcnow().date()).order_by('-data_usage')[:100]
    context = {'userlogs': userloglist_qs}
    return render_to_response('top-users-bw.html', context)

def bw_report_ips(request):
    iploglist_qs = IPLog.objects.filter(date=datetime.datetime.utcnow().date()).order_by('-data_usage')[:100]
    context = {'iplogs': iploglist_qs}
    return render_to_response('top-ips-bw.html', context)

def deny_count_report_users(request):
    userloglist_qs = UserLog.objects.filter(date=datetime.datetime.utcnow().date()).order_by('-deny_count')[:100]
    context = {'userlogs': userloglist_qs}
    return render_to_response('top-users-deny-count.html', context)
    
def deny_count_report_ips(request):
    iploglist_qs = IPLog.objects.filter(date=datetime.datetime.utcnow().date()).order_by('-deny_count')[:100]
    context = {'iplogs': iploglist_qs}
    return render_to_response('top-ips-deny-count.html', context)

def json_data(request, type=""):
    import json
    dict_result = {"aaData": []}

    userloglist_qs = None
    iploglist_qs = None

    if type == "top-users-bw":
        userloglist_qs = UserLog.objects.filter(date=datetime.datetime.utcnow().date()).order_by('-data_usage')[:100]
    elif type == "top-users-deny-count":
        userloglist_qs = UserLog.objects.filter(date=datetime.datetime.utcnow().date()).order_by('-deny_count')[:100]

    if type ==  "top-ips-bw":
        iploglist_qs = IPLog.objects.filter(date=datetime.datetime.utcnow().date()).order_by('-data_usage')[:100]
    elif type ==  "top-ips-deny-count":
        iploglist_qs = IPLog.objects.filter(date=datetime.datetime.utcnow().date()).order_by('-deny_count')[:100]

    if userloglist_qs != None:
        for obj in userloglist_qs:
            (dict_result['aaData']).append({
                'username': obj.username,
                'date': obj.date.strftime(format="%a %d %b %Y"),
                'data_usage': "%3f" % (float(obj.data_usage)/1048576),
                'denied_data_size': "%3f" % (float(obj.denied_data_size)/1048576),
                'deny_count': str(obj.deny_count),
                'first_access': obj.first_access.strftime(format="%H:%M:%S %d-%m-%Y"),
                'last_access': obj.last_access.strftime(format="%H:%M:%S %d-%m-%Y"),
            })

    elif iploglist_qs !=None:
        for obj in iploglist_qs:
            (dict_result['aaData']).append({
                'ip_addr': obj.ip_addr,
                'date': obj.date.strftime(format="%a %d %b %Y"),
                'data_usage': "%3f" % (float(obj.data_usage)/1048576),
                'denied_data_size': "%3f" % (float(obj.denied_data_size)/1048576),
                'deny_count': str(obj.deny_count),
                'first_access': obj.first_access.strftime(format="%H:%M:%S %d-%m-%Y"),
                'last_access': obj.last_access.strftime(format="%H:%M:%S %d-%m-%Y"),
            })
    return HttpResponse(json.dumps( dict_result , sort_keys=True, indent=4, separators=(',', ': ') ), content_type="application/json")

def index(request):
    return bw_report_users(request)
