from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'fm.web.views.home', name='fm.home'),
    url(r'^administradores$', 'fm.web.views.administrators_list', name='administrators_list'),
    url(r'^fondos-mutuos/(?P<administrator_id>\d+)/(?P<slug>[A-Za-z0-9\-]+)/$', 'fm.web.views.mutual_funds_by_administrator', name='mutual_funds_by_administrator'),
    url(r'^fondo-mutuo/(?P<mutual_fund_id>\d+)/(?P<slug>[A-Za-z0-9\-]+)/$', 'fm.web.views.mutual_fund_detail', name='mutual_fund_detail'),
    url(r'^fondo-mutuo/chart-data$', 'fm.web.views.mutual_fund_chart_data'),
)

urlpatterns += staticfiles_urlpatterns()
