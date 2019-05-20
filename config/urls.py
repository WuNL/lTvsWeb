from django.conf.urls import url
import config.views

urlpatterns = [
	url(r'^textStyle/', config.views.textStyleView),
	url(r'^getMonitorInfo/', config.views.getMonitorInfo),
	url(r'^configSystem/', config.views.configSystem),
	url(r'^log/', config.views.logView),
	url(r'^exportUserLogAsCSV/$', config.views.exportUserLogAsCSV),
    url(r'^clearUserLog/$', config.views.clearUserLog),
]
