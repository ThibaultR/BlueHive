from tastypie.resources import ModelResource
from tastypie.paginator import Paginator
from BlueHive.models import CustomUser
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization


from BlueHive.models import Event, EventRequest

class UserResource(ModelResource):
    class Meta:
        queryset = CustomUser.objects.all()
        resource_name = 'user'
        #fields = ['email', 'first_name', 'last_name', 'rating']
        allowed_methods = ['get']

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        paginator_class = Paginator
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()


class EventRequestResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user_id')
    class Meta:
        queryset = EventRequest.objects.all()
        resource_name = 'event_request'


