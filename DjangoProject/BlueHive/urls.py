from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', 'BlueHive.views.user_login'),
    url(r'^user/login/$', 'BlueHive.views.user_login', name='user_login'),
    url(r'^user/logout/$', 'BlueHive.views.user_logout', name='user_logout'),
    url(r'^user/register/$', 'BlueHive.views.user_register', name='user_register'),
    url(r'^user/data/set_profile_picture/(?P<user_id>\d+)/$', 'BlueHive.views.user_data_set_profile_picture', name='user_data_set_profile_picture'),
    url(r'^user/data/get_profile_picture/(?P<user_id>\d+)/$', 'BlueHive.views.user_data_get_profile_picture', name='user_data_get_profile_picture'),
    url(r'^user/register_success/$', 'BlueHive.views.user_register_success', name='user_register_success'),
    url(r'^user/data/$', 'BlueHive.views.user_data', name='user_data'),
    url(r'^user/events/$', 'BlueHive.views.user_events', name='user_events'),
    url(r'^user/$', 'BlueHive.views.user_events', name='user_events'),
    url(r'^user/events/edit_comment/$', 'BlueHive.views.user_events_edit_comment', name='user_events_edit_comment'),
    url(r'^user/events/(?P<event_id>\d+)/$', 'BlueHive.views.user_events_apply', name='user_events_apply'),
    url(r'^event/overview/$', 'BlueHive.views.event_overview', name='event_overview'),
    url(r'^event/add/$', 'BlueHive.views.event_add', name='event_add'),
    url(r'^event/edit/(?P<event_id>\d+)/$', 'BlueHive.views.event_edit', name='event_edit'),
    url(r'^event/status/$', 'BlueHive.views.event_status', name='event_status'),
    url(r'^event/deactivate/$', 'BlueHive.views.event_deactivate', name='event_deactivate'),
    url(r'^group/$', 'BlueHive.views.group_overview', name='group_overview'),
    url(r'^group/overview/$', 'BlueHive.views.group_overview', name='group_overview2'),
    url(r'^group/add/$', 'BlueHive.views.group_add', name='group_add'),
    url(r'^group/edit/$', 'BlueHive.views.group_edit', name='group_edit'),
    url(r'^admin/users/$', 'BlueHive.views.admin_users', name='admin_users'),
    url(r'^admin/users/status/$', 'BlueHive.views.admin_users_status', name='admin_users_status'),
    url(r'^admin/users/edit/(?P<user_id>\d+)/$', 'BlueHive.views.admin_users_edit', name='admin_users_edit'),

    url(r'^group/delete/(?P<group_id>\d+)/$', 'BlueHive.views.group_delete', name='group_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
