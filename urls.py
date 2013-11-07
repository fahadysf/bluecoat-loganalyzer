from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'bcloganalyzer.frontend.views.index', name='index'),
    url(r'^bw-users/$', 'bcloganalyzer.frontend.views.bw_report_users', name='bw_report_users'),
    url(r'^deny-count-users/$', 'bcloganalyzer.frontend.views.deny_count_report_users', name='bw_report_ips'),
    url(r'^bw-unauthenticated-ips/$', 'bcloganalyzer.frontend.views.bw_report_ips', name='deny_count_report_users'),
    url(r'^deny-count-unauthenticated-ips/', 'bcloganalyzer.frontend.views.deny_count_report_ips', name='deny_count_report_ips'),
    url(r'^json_data/(?P<type>\S+)/', 'bcloganalyzer.frontend.views.json_data'),
     #url(r'^data/', include('bcloganalyzer.foo.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
