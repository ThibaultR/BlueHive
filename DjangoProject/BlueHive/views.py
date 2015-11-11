from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth import views
from django.views.generic.base import TemplateView
from BlueHive.models import Event
from forms import MyRegistrationForm
from forms import EventForm
from forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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
        return HttpResponseRedirect('/user/loggedin')
    else:
        return HttpResponseRedirect('/user/invalid')

def user_loggedin(request):
    return render_to_response('BlueHive/user/loggedin.html', {'full_name': request.user.username})

def user_invalid_login(request):
    return render_to_response('BlueHive/user/invalid_login.html')

def user_logout(request):
    auth.logout(request)
    return render_to_response("BlueHive/user/logout.html")


def user_register(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/register_success')
    args = {}
    args.update(csrf(request))

    args['form'] = MyRegistrationForm()

    return render_to_response('BlueHive/user/register.html', args)

def user_register_success(request):
    return render_to_response('BlueHive/user/register_success.html')

def event_add(request):
    if request.POST:
        form =EventForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/event/overview')
    else:
        form = EventForm()

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

@login_required
def user_data(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/loggedin')
    else:
        user = request.user
        profile =user.profile
        form = UserProfileForm(instance=profile)

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response(('BlueHive/user/user_data.html', args))




