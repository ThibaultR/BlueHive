from django.conf.urls import url

from . import views

''' part for user registration, user events and user data ''',

#url(r'^user/events/', 'BlueHive.views.user_events', name='user_events'),
#url(r'^user/data/', 'BlueHive.views.user_data', name='user_data'),
''' part for event management by administrator '''
urlpatterns = [
    url(r'^$', 'BlueHive.views.user_login'),
    url(r'^user/login/', 'BlueHive.views.user_login', name='user_login'),
    url(r'^user/auth/', 'BlueHive.views.user_auth', name='user_auth'),
    url(r'^user/logout/', 'BlueHive.views.user_logout', name='user_logout'),
    url(r'^user/loggedin/', 'BlueHive.views.user_loggedin', name='user_loggedin'),
    url(r'^user/invalid/', 'BlueHive.views.user_invalid_login', name='user_invalid_login'),
    url(r'^user/register/', 'BlueHive.views.user_register', name='user_register'),
    url(r'^user/register_success/', 'BlueHive.views.user_register_success', name='user_register_success'),
    url(r'^user/data/', 'BlueHive.views.user_data', name='user_data'),
    url(r'^event/overview', 'BlueHive.views.event_overview', name='event_overview'),
    url(r'^event/add', 'BlueHive.views.event_add', name='event_add'),
    url(r'^event/(?P<event_id>\d+)/$', 'BlueHive.views.event', name='event'),
]