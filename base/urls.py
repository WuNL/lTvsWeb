from django.conf.urls import url
import base.views
urlpatterns = [
	url(r'^$', base.views.homeView),
    url(r'^configChannels/', base.views.configChannels),
    url(r'^addTerminals/', base.views.addTerminals),
    url(r'^editTerminals/(?P<terminalID>\d+)/$', base.views.editTerminals),
    url(r'^deleteTerminal/(?P<terminalID>\d+)/$', base.views.deleteTerminal),
    url(r'^configChannel/(?P<channelID>\d+)/$', base.views.configChannel),
    url(r'^configChannel/(?P<channelID>\d+)/(?P<channelNum>\d+)/$', base.views.configChannelWithNum),
    url(r'^configPolling/(?P<channelID>\d+)/(?P<channelNum>\d+)/$', base.views.configPolling),

	url(r'^hsInterface/', base.views.hsInterface),
]
