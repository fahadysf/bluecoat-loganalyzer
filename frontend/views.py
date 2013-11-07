# Create your views here.

import time,datetime

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
    
def index(request):
    return bw_report_users(request)