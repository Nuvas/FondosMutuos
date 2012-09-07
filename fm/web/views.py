from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from fm.web.models import *

def home(request):
    return redirect('administrators_list')

def administrators_list(request):
    administrators = Administrator.objects.all()
    return render_to_response('administrators_list.html', locals())

def mutual_funds_by_administrator(request, administrator_id, slug):
    administrator = get_object_or_404(Administrator, pk=administrator_id)
    mutual_funds = MutualFund.objects.filter(administrator = administrator)
    return render_to_response('mutual_funds_by_administrator.html', locals())

def mutual_fund_detail(request, mutual_fund_id, slug):
    mutual_fund = get_object_or_404(MutualFund, pk=mutual_fund_id)
    day = mutual_fund.get_last_day()
    return render_to_response('mutual_fund_detail.html', locals())

def mutual_fund_chart_data(request):
    mutual_fund_id = request.GET.get('id')
    mutual_fund = get_object_or_404(MutualFund, pk=mutual_fund_id)
    data = mutual_fund.get_line_data()
    return HttpResponse(data)
