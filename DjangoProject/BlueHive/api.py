from tastypie.paginator import Paginator
from BlueHive.models import CustomUser
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource, ALL

from BlueHive.models import Event, EventRequest

class UserResource(ModelResource):
    class Meta:
        queryset = CustomUser.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']



class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        paginator_class = Paginator
        authentication = ApiKeyAuthentication()


class EventRequestResource(ModelResource):
    user_id = fields.ForeignKey(UserResource, 'user_id')
    class Meta:
        queryset = EventRequest.objects.all()
        resource_name = 'event_request'
        authentication = ApiKeyAuthentication()
        filtering = {
            'user_id': ALL,
        }


