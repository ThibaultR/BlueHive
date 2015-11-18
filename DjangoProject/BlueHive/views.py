from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth import views
from BlueHive.models import Event, UserGroup, EventRequest
from forms import EventForm
from forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
# Create your views here.



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
                myEventRequest.save()
    except Event.DoesNotExist:
        print 'Event with this id doesn\'t exist'

    return HttpResponseRedirect('/user/events')


@login_required
def user_events(request):
    # check events which have a group where user is part of
    user_groups = request.user.user_group.all()
    applied_events = EventRequest.objects.filter(user_id=request.user, event_id__begin_time__gte=timezone.now()+timezone.timedelta(days=-2)).exclude(event_id__status=-1)
    applied_events_ids = EventRequest.objects.values_list('event_id', flat=True).filter(user_id=request.user)
    new_events = Event.objects.filter(user_group=user_groups, begin_time__gte=timezone.now()+timezone.timedelta(days=-2)).exclude(id__in=applied_events_ids).exclude(status=-1)
    return render_to_response('BlueHive/user/user_events.html', {'new_events': new_events, 'applied_events':applied_events})


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


