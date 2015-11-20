from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth import views
from BlueHive.models import Event, UserGroup, EventRequest,CustomUser
from forms import EventForm, UserGroupForm
from forms import CustomUserChangeForm, CustomUserCreationForm,EventRequestForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic.edit import UpdateView
from django.template import RequestContext

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from models import Author

# Create your views here.
def handler404(request):
    response = render_to_response('BlueHive/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response



def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    return template_response


def user_login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('BlueHive/user/login.html', c)

def user_auth(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/user/events')
    else:
        return HttpResponseRedirect('/user/invalid')


def user_invalid_login(request):
    return render_to_response('BlueHive/user/invalid_login.html')

def user_logout(request):
    auth.logout(request)
    return render_to_response("BlueHive/user/logout.html")


def user_register(request):
    if request.method == 'POST':
        #form = CustomUserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            default_group = UserGroup.objects.get(id=1)
            new_user.user_group.add(default_group)
            form.save_m2m()
            return HttpResponseRedirect('/user/register_success')
        else:
            #render_to_response('BlueHive/user/register.html', {'form': form})
            print form.errors #To see the form errors in the console.
            return render(request, 'BlueHive/user/register.html', {'form': form})
    args = {}
    args.update(csrf(request))

    args['form'] = CustomUserCreationForm()

    return render_to_response('BlueHive/user/register.html', args)



def user_register_success(request):
    return render_to_response('BlueHive/user/register_success.html')


@login_required
def user_data(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/events')
        else:
            print form.errors
            return render(request, 'BlueHive/user/user_data.html', {'form': form})
    else:
        form = CustomUserChangeForm(instance=request.user)
        args = {}
        args.update(csrf(request))

        args['form'] = form

        return render_to_response('BlueHive/user/user_data.html', args)


@login_required
def user_events_apply(request, event_id):
    event_id = int(event_id)
    if request.method == 'POST':
        #TODO security of user_comment parameter
        user_comment = request.POST.get('user_comment')
        # check if user is allowed to be part of this event
        try:
            event = Event.objects.get(id=event_id)
            # compare if event is in the right status, date and a group where the user is also part in
            if event.status != -1 and event.begin_time >= timezone.now() and request.user.user_group.all().filter(value=event.user_group).exists():
                # check if there is already an EventRequest for this event
                try:
                    EventRequest.objects.get(event_id=event_id, user_id=request.user.id)
                except EventRequest.DoesNotExist:
                    #now the new Eventrequest can be created
                    myEventRequest = EventRequest()
                    myEventRequest.event_id = event
                    myEventRequest.user_id = request.user
                    myEventRequest.user_comment = user_comment
                    myEventRequest.save()
        except Event.DoesNotExist:
            print 'Event with this id doesn\'t exist'

    return HttpResponseRedirect('/user/events/')


@login_required
def user_events(request):
    args = {}
    args.update(csrf(request))

# check events which have a group where user is part of
    user_groups = request.user.user_group.all()
    args['applied_events'] = EventRequest.objects.filter(user_id=request.user, event_id__begin_time__gte=timezone.now()+timezone.timedelta(days=-2)).exclude(event_id__status=-1)
    applied_events_ids = EventRequest.objects.values_list('event_id', flat=True).filter(user_id=request.user)
    args['new_events'] = Event.objects.filter(user_group=user_groups, begin_time__gte=timezone.now()+timezone.timedelta(days=-2)).exclude(id__in=applied_events_ids).exclude(status=-1)
    return render_to_response('BlueHive/user/user_events.html', args)


def user_events_edit_comment(request):
    if request.POST:
        user_comment = request.POST.get('value')
        event_id = request.POST.get('id')
        user_id = request.user.id
        data = {'event_id': event_id, 'user_id': user_id,  'user_comment': user_comment}
        form = EventRequestForm(data)

        if form.is_valid():
            try:
                myEventRequest = EventRequest.objects.get(event_id=event_id, user_id=user_id)
                myEventRequest.user_comment = user_comment
                myEventRequest.save()
            except EventRequest.DoesNotExist:
                return HttpResponse(user_comment)

        else:
            return HttpResponse(user_comment)


        return HttpResponse(user_comment)
    return HttpResponseRedirect('/user/events')


def event_add(request):
    if request.POST:
        form =EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/event/overview')
        else:
            return render(request, 'BlueHive/event/event_add.html', {'form': form})
    else:
        form = EventForm(initial={'location': 'LTU Lulea'})

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render_to_response('BlueHive/event/event_add.html', args)


def event(request, event_id):
    return render_to_response('BlueHive/event/event_detail.html', {'event': Event.objects.get(id=event_id)})


def event_overview(request):
    return render_to_response('BlueHive/event/event_overview.html', {'events': Event.objects.all()})

def event_deactivate(request, event_id):
    if event_id:
        e = Event.objects.get(id=event_id)
        e.status = -1
        e.save()
        return HttpResponseRedirect('/event/overview')


def group_overview(request):
    args = {}
    args.update(csrf(request))
    args['newusergroupform'] = UserGroupForm()
    args['groups'] = UserGroup.objects.all()


    return render_to_response('BlueHive/group/group_overview.html', args)


def group_add(request):
    if request.POST:
        form =UserGroupForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'BlueHive/group/group_overview.html', {'newusergroupform': form, 'groups': UserGroup.objects.all()})
    return HttpResponseRedirect('/group/overview')


def group_edit(request):
    if request.POST:
        id = request.POST.get('id')
        value = request.POST.get('value')
        usergroup = get_object_or_404(UserGroup, pk=id)
        usergroup.value = value
        usergroup.save()
        return HttpResponse(value)
    return HttpResponseRedirect('/group/overview')

def group_delete(request, group_id):
    if group_id != '1':
        # no user should be member of the group any more, automatically done by django when deleting group
        # all events which belong to this group belong to the default group with id 1
        Event.objects.filter(user_group=group_id).update(user_group=1)
        # delete the group itself
        UserGroup.objects.filter(id=group_id).delete()
    return HttpResponseRedirect('/group/overview')


def admin_users(request):
    args = {}
    args.update(csrf(request))
    args['new_users'] = CustomUser.objects.filter()
    args['groups'] = UserGroup.objects.all()


    return render_to_response('BlueHive/group/group_overview.html', args)
