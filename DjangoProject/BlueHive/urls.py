from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls import (handler400, handler403, handler404, handler500)
from django.core.urlresolvers import reverse
urlpatterns = [
    url(r'^$', 'BlueHive.views.user_login'),
    url(r'^user/login/', 'BlueHive.views.user_login', name='user_login'),
    url(r'^user/auth/', 'BlueHive.views.user_auth', name='user_auth'),
    url(r'^user/logout/', 'BlueHive.views.user_logout', name='user_logout'),
    url(r'^user/invalid/', 'BlueHive.views.user_invalid_login', name='user_invalid_login'),
    url(r'^user/register/$', 'BlueHive.views.user_register', name='user_register'),
    url(r'^user/register/picture/$', 'BlueHive.views.user_register_picture', name='user_register_picture'),
    url(r'^user/register_success/', 'BlueHive.views.user_register_success', name='user_register_success'),
    url(r'^user/data/$', 'BlueHive.views.user_data', name='user_data'),
    url(r'^user/data/profile_picture/$', 'BlueHive.views.user_data_profile_picture', name='user_data_profile_picture'),
    url(r'^user/events/$', 'BlueHive.views.user_events', name='user_events'),
    url(r'^user/events/edit_comment/$', 'BlueHive.views.user_events_edit_comment', name='user_events_edit_comment'),
    url(r'^user/events/(?P<event_id>\d+)/$', 'BlueHive.views.user_events_apply', name='user_events_apply'),
    url(r'^event/overview', 'BlueHive.views.event_overview', name='event_overview'),
    url(r'^event/add', 'BlueHive.views.event_add', name='event_add'),
    url(r'^event/(?P<event_id>\d+)/$', 'BlueHive.views.event', name='event'),
    url(r'^group/$', 'BlueHive.views.group_overview', name='group_overview'),
    url(r'^group/overview/$', 'BlueHive.views.group_overview', name='group_overview2'),
    url(r'^group/add/$', 'BlueHive.views.group_add', name='group_add'),
    url(r'^group/edit/$', 'BlueHive.views.group_edit', name='group_edit'),
    url(r'^admin/users/$', 'BlueHive.views.admin_users', name='admin_users'),

    url(r'^group/delete/(?P<group_id>\d+)/$', 'BlueHive.views.group_delete', name='group_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#handler404 = 'views.page_not_found'

#handler400 = 'views.bad_request'
#handler403 = 'views.permission_denied'
#handler500 = 'views.server_error'
