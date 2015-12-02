from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from django.core.context_processors import csrf
from BlueHive.models import Event, UserGroup, EventRequest, CustomUser, NewProfilePicture
from BlueHive.forms import EventForm, UserGroupForm, CustomUserChangeForm, CustomUserCreationForm, EventRequestForm, \
    NewProfilePictureForm, AdminCustomUserChangeForm
from BlueHive.forms import AdminChangePasswordForm, UserChangePasswordForm
from django.utils import timezone
from django.conf import settings
from django.template import RequestContext
from django.middleware.csrf import rotate_token  # for changing csrf token
import shutil, os


def admin_check(user):
    return user.is_superuser == 1


def active_user_check(user):
    return user.account_status == 1


def user_login(request):
    # message = "Please log in ..."
    message = ""
    if request.user.is_authenticated():
        auth.logout(request)

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=email, password=password)

        if user is not None:
            if user.is_superuser == 1:
                auth.login(request, user)
                return HttpResponseRedirect('/event/overview/')
            if user.account_status == -1:
                message = "Your account is blocked."
            if user.account_status == 0:
                message = "Your account is not active, please wait until you are activated."
            if user.account_status == 1:
                auth.login(request, user)
                return HttpResponseRedirect('/user/events/')
        else:
            message = "Your username/password combination doesn't exist."
    args = {}
    args['message'] = message
    args.update(csrf(request))
    return render_to_response('BlueHive/user/login.html', args)


def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/user/login/')


def user_register(request):
    if request.user.is_authenticated():
        auth.logout(request)
    if request.method == 'POST':
        # form = CustomUserCreationForm(request.POST, request.FILES)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            # check if the image for the user is here
            try:
                profile_picture_old_path = NewProfilePicture.objects.get(csrftoken=request.META["CSRF_COOKIE"])
                new_user = form.save(commit=False)
                new_user.save()

                # put the picture to the right place and save it for the user
                basic_path = settings.MEDIA_ROOT + '/profile_pictures/'
                profile_picture_new_path = basic_path + str(new_user.id) + '.jpg'
                if not os.path.exists(basic_path):
                    os.makedirs(basic_path)
                shutil.copy2(str(profile_picture_old_path), profile_picture_new_path)

                # delete the old folder containing the pictures of that user
                shutil.rmtree(settings.MEDIA_ROOT + '/new_pictures/' + request.META["CSRF_COOKIE"])

                new_user.profile_picture = profile_picture_new_path
                new_user.save()
                default_group = UserGroup.objects.get(id=1)
                new_user.user_group.add(default_group)
                form.save_m2m()

            except NewProfilePicture.DoesNotExist:
                print 'There is no profile picture for this user'
                return render(request, 'BlueHive/user/register.html',
                              {'form': form, 'picturemissing': 'Please upload a profile picture!'})

            return HttpResponseRedirect('/user/register_success')
        else:
            # render_to_response('BlueHive/user/register.html', {'form': form})
            print form.errors  # To see the form errors in the console.
            return render(request, 'BlueHive/user/register.html', {'form': form})
    rotate_token(request)
    args = {}
    args.update(csrf(request))

    args['form'] = CustomUserCreationForm()

    return render_to_response('BlueHive/user/register.html', args)


def user_data_set_profile_picture(request, user_id):
    if request.method == 'POST':
        csrftoken = request.META["CSRF_COOKIE"]
        request.POST['csrftoken'] = csrftoken
        form = NewProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            # when the picture comes from a already registered user
            if request.user.id:
                actUser = get_object_or_404(CustomUser, pk=request.user.id)
                # check if the request comes from the admin
                if actUser.is_superuser == 1:
                    # now we can trust the user_id param
                    actUser = get_object_or_404(CustomUser, pk=user_id)

                # check if there is already another picture of this csrftoken and delete it if yes
                old_profile_pictures = NewProfilePicture.objects.filter(user_id=actUser.id)
                if old_profile_pictures.count() > 0:
                    old_profile_pictures.delete()

                new_file = NewProfilePicture(file=request.FILES['file'], csrftoken=csrftoken, user_id=actUser.id)
                new_file.save(extra_param=csrftoken)

                # now set the new picture as actual picture
                profile_picture_old_path = NewProfilePicture.objects.get(user_id=actUser.id)

                # put the picture to the right place and save it for the user
                basic_path = settings.MEDIA_ROOT + '/profile_pictures/'
                profile_picture_new_path = basic_path + str(actUser.id) + '.jpg'
                if not os.path.exists(basic_path):
                    os.makedirs(basic_path)
                shutil.copy2(str(profile_picture_old_path), profile_picture_new_path)

                # delete the old folder containing the pictures of that user
                shutil.rmtree(settings.MEDIA_ROOT + '/new_pictures/' + request.META["CSRF_COOKIE"])

                actUser.profile_picture = profile_picture_new_path
                actUser.save()

                return HttpResponse(status=200)

            else:
                # check if there is already another picture of this csrftoken and delete it if yes
                old_profile_pictures = NewProfilePicture.objects.filter(csrftoken=request.META["CSRF_COOKIE"])
                if old_profile_pictures.count() > 0:
                    old_profile_pictures.delete()

                new_file = NewProfilePicture(file=request.FILES['file'], csrftoken=csrftoken)
                new_file.save(extra_param=csrftoken)
                return HttpResponse(status=200)

        else:
            print form.errors
            return HttpResponse(status=500)

    return HttpResponseRedirect('/user/register/')


@login_required
def user_data_get_profile_picture(request, user_id):
    if request.method == 'POST':
        actUser = get_object_or_404(CustomUser, pk=request.user.id)
        # check if the request comes from the admin
        if actUser.is_superuser == 1:
            # now we can trust the user_id param
            actUser = get_object_or_404(CustomUser, pk=user_id)
        # lot of help from http://stackoverflow.com/questions/18048825/how-to-limit-the-number-of-dropzone-js-files-uploaded?rq=1
        # TODO check validity
        picture_path = '/media/' + str(CustomUser.objects.get(id=actUser.id).profile_picture)
        picture_size = os.path.getsize(str(CustomUser.objects.get(id=actUser.id).profile_picture))
        return JsonResponse({'name': picture_path, 'size': picture_size})

    return HttpResponseRedirect('/user/data/')


def user_register_success(request):
    return render_to_response('BlueHive/user/register_success.html')


@login_required
def user_data(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        password_form = UserChangePasswordForm(request.user, request.POST)
        newPassword = False
        formError = False
        if len(request.POST.get('new_password1')) > 1:
            if password_form.is_valid():
                newPassword = True
            else:
                print password_form.errors
                formError = True

        if form.is_valid() and not formError:
            form.save()
            if newPassword:
                new_password = password_form.cleaned_data['new_password2']
                user = get_object_or_404(CustomUser, pk=request.user.id)
                user.set_password(new_password)
                user.save()
            return HttpResponseRedirect('/user/events')
        else:
            print form.errors
            return render(request, 'BlueHive/user/user_data.html', {'form': form, 'password_form': password_form})
    else:
        form = CustomUserChangeForm(instance=request.user)
        password_form = UserChangePasswordForm(request.user)
        args = {}
        args.update(csrf(request))

        args['form'] = form
        args['password_form'] = password_form

        return render_to_response('BlueHive/user/user_data.html', args)


@user_passes_test(admin_check)
def admin_users_edit(request, user_id):
    if request.method == 'POST':
        form = AdminCustomUserChangeForm(request.POST, request.FILES,
                                         instance=get_object_or_404(CustomUser, pk=user_id))
        password_form = AdminChangePasswordForm(request.POST)
        newPassword = False
        formError = False
        if len(request.POST.get('new_password1')) > 1:
            if password_form.is_valid():
                newPassword = True
            else:
                print password_form.errors
                formError = True
        if form.is_valid() and not formError:
            form.save()
            if newPassword:
                new_password = password_form.cleaned_data['new_password2']
                user = get_object_or_404(CustomUser, pk=user_id)
                user.set_password(new_password)
                user.save()
            return HttpResponseRedirect('/admin/users/')
        else:
            print form.errors
            return render(request, 'BlueHive/admin/admin_users_edit.html',
                          {'form': form, 'password_form': password_form})
    else:
        form = AdminCustomUserChangeForm(instance=get_object_or_404(CustomUser, pk=user_id))
        # http://ruddra.com/2015/09/18/implementation-of-forgot-reset-password-feature-in-django/
        password_form = AdminChangePasswordForm()
        args = {}
        args.update(csrf(request))

        args['form'] = form
        args['password_form'] = password_form
        args['user_id'] = user_id

    return render_to_response('BlueHive/admin/admin_users_edit.html', args)


@login_required
def user_events_apply(request, event_id):
    event_id = int(event_id)
    if request.method == 'POST':
        # TODO security of user_comment parameter
        user_comment = request.POST.get('user_comment')
        # check if user is allowed to be part of this event
        try:
            event = Event.objects.get(id=event_id)
            # compare if event is in the right status, date and a group where the user is also part in
            if event.status != -1 and event.begin_time >= timezone.now() and request.user.user_group.all().filter(
                    value=event.user_group).exists():
                # check if there is already an EventRequest for this event
                try:
                    EventRequest.objects.get(event_id=event_id, user_id=request.user.id)
                except EventRequest.DoesNotExist:
                    # now the new Eventrequest can be created
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
    args['applied_events'] = EventRequest.objects.filter(user_id=request.user,
                                                         event_id__begin_time__gte=timezone.now() + timezone.timedelta(
                                                             days=-2)).exclude(event_id__status=-1)
    applied_events_ids = EventRequest.objects.values_list('event_id', flat=True).filter(user_id=request.user).order_by(
        'begin_time', 'name')
    args['new_events'] = Event.objects.filter(user_group=user_groups,
                                              begin_time__gte=timezone.now() + timezone.timedelta(days=-2)).exclude(
        id__in=applied_events_ids).exclude(status=-1).order_by('begin_time', 'name')
    return render_to_response('BlueHive/user/user_events.html', args)


@login_required
def user_events_edit_comment(request):
    if request.POST:
        user_comment = request.POST.get('value')
        event_id = request.POST.get('id')
        user_id = request.user.id
        data = {'event_id': event_id, 'user_id': user_id, 'user_comment': user_comment}
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


@user_passes_test(admin_check)
def event_add(request):
    if request.POST:
        form = EventForm(request.POST)
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


@user_passes_test(admin_check)
def event(request, event_id):
    return render_to_response('BlueHive/event/event_detail.html', {'event': Event.objects.get(id=event_id)})


@user_passes_test(admin_check)
def event_overview(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        for key, value in request.POST.iteritems():
            if key.startswith('user'):
                user_id = key[7:]
                actEventRequest = EventRequest.objects.get(event_id=event_id, user_id=user_id)
                if value == 'rejected':
                    actEventRequest.status = -1
                    actEventRequest.save()
                if value == 'waiting':
                    actEventRequest.status = 0
                    actEventRequest.save()
                if value == 'accepted':
                    actEventRequest.status = 1
                    actEventRequest.save()
    # https://docs.djangoproject.com/en/1.8/ref/templates/builtins/#date
    args = {}
    args.update(csrf(request))
    events = Event.objects.filter(begin_time__gte=timezone.now() + timezone.timedelta(days=-2)).exclude(
        status=-1).order_by('begin_time', 'name')
    event_request = EventRequest.objects.filter(event_id__in=events.values("id"))
    args['events'] = events
    args['event_request'] = event_request

    return render_to_response('BlueHive/event/event_overview.html', args)


@user_passes_test(admin_check)
def event_deactivate(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, pk=event_id)
        event.status = -1
        event.save()
    return HttpResponseRedirect(reverse('BlueHive:event_overview'))


@user_passes_test(admin_check)
def event_edit(request, event_id):
    if request.method == 'POST':
        form = EventForm(request.POST, instance=get_object_or_404(Event, pk=event_id))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('BlueHive:event_overview'))
        else:
            print form.errors
            return render(request, 'BlueHive/event/event_edit.html', {'form': form})
    else:
        form = EventForm(instance=get_object_or_404(Event, pk=event_id))
        args = {}
        args.update(csrf(request))

        args['form'] = form
        args['event_id'] = event_id
        return render_to_response('BlueHive/event/event_edit.html', args)


@user_passes_test(admin_check)
def event_status(request):
    if request.POST:
        value = request.POST.get('value')
        event_id = request.POST.get('event_id')
        actEvent = get_object_or_404(Event, pk=event_id)
        if value == 'deactivate':
            actEvent.status = -1
            actEvent.save()

    return HttpResponseRedirect(reverse('BlueHive:event_overview'))


@user_passes_test(admin_check)
def group_overview(request):
    args = {}
    args.update(csrf(request))
    args['newusergroupform'] = UserGroupForm()
    args['groups'] = UserGroup.objects.all()

    return render_to_response('BlueHive/group/group_overview.html', args)


@user_passes_test(admin_check)
def group_add(request):
    if request.POST:
        form = UserGroupForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'BlueHive/group/group_overview.html',
                          {'newusergroupform': form, 'groups': UserGroup.objects.all()})
    return HttpResponseRedirect('/group/overview')


@user_passes_test(admin_check)
def group_edit(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        value = request.POST.get('value')
        usergroup = get_object_or_404(UserGroup, pk=id)
        usergroup.value = value
        usergroup.save()
        return HttpResponse(value)
    return HttpResponseRedirect('/group/overview')


@user_passes_test(admin_check)
def group_delete(request, group_id):
    if group_id != '1':
        # no user should be member of the group any more, automatically done by django when deleting group
        # all events which belong to this group belong to the default group with id 1
        Event.objects.filter(user_group=group_id).update(user_group=1)
        # delete the group itself
        UserGroup.objects.filter(id=group_id).delete()
    return HttpResponseRedirect('/group/overview')


@user_passes_test(admin_check)
def admin_users(request):
    args = {}
    args.update(csrf(request))
    # args['user'] = request.user
    args['new_users'] = CustomUser.objects.filter(account_status=0, is_superuser=0).order_by('last_name', 'first_name')
    args['active_users'] = CustomUser.objects.filter(account_status=1, is_superuser=0).order_by('last_name',
                                                                                                'first_name')
    args['deactivated_users'] = CustomUser.objects.filter(account_status=-1, is_superuser=0).order_by('last_name',
                                                                                                      'first_name')

    return render_to_response('BlueHive/admin/admin_users.html', args)


@user_passes_test(admin_check)
def admin_users_status(request):
    if request.method == 'POST':
        value = request.POST.get('value')
        user_id = request.POST.get('user_id')
        actUser = get_object_or_404(CustomUser, pk=user_id)
        if value == 'activate':
            # activate this user when his actual account_status == 0
            if actUser.account_status == 0 or actUser.account_status == -1:
                actUser.account_status = 1
                actUser.save()
                return HttpResponseRedirect('/admin/users/')
        elif value == 'deactivate':
            # delete this user when his actual account_status == 0
            if actUser.account_status == 1:
                # TODO what happens with the events of the user
                actUser.account_status = -1
                actUser.save()
                return HttpResponseRedirect('/admin/users/')
        elif value == 'delete':
            # delete this user when his actual account_status == 0
            if actUser.account_status == 0:
                actUser.delete()
                return HttpResponseRedirect('/admin/users/')
        elif value == 'edit':
            # edit this user when his actual account_status != 0
            if actUser.account_status != 0:
                return HttpResponseRedirect('/admin/users/edit/' + user_id)
        elif value == 'show':
            if actUser.account_status < 2:
                return HttpResponseRedirect('/admin/users/edit/' + user_id)

    return HttpResponseRedirect('/admin/users/')
