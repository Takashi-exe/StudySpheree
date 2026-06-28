from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudyGroup, GroupMembership, GroupChatMessage, GroupResource
from .forms import GroupForm, GroupResourceForm
from studySessions.models import StudySession
from django.db.models import Prefetch

@login_required
def group_list(request):
    groups = request.user.study_groups.all().select_related('created_by')
    return render(request, 'groups/group_list.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            GroupMembership.objects.create(user=request.user, group=group, role='admin')
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('groups:group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'groups/group_form.html', {'form': form})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(
        StudyGroup.objects.prefetch_related(
            'members__profile', 
            'chat_messages__user__profile', 
            'resources__uploaded_by__profile'
        ), 
        id=group_id
    )
    
    if request.method == 'POST' and 'content' in request.POST:
        content = request.POST.get('content')
        if content:
            GroupChatMessage.objects.create(group=group, user=request.user, content=content)
            return redirect('groups:group_detail', group_id=group.id)

    # Use Prefetch to get participants for active sessions
    active_session_prefetch = Prefetch(
        'sessions',
        queryset=StudySession.objects.filter(is_active=True).prefetch_related('participants__profile'),
        to_attr='active_sessions_list'
    )
    group_with_active_session = StudyGroup.objects.prefetch_related(active_session_prefetch).get(id=group_id)
    active_session = group_with_active_session.active_sessions_list[0] if group_with_active_session.active_sessions_list else None

    past_group_sessions = StudySession.objects.filter(group=group, is_active=False).order_by('-start_time')[:5]
    user_study_history = StudySession.objects.filter(participants=request.user, is_active=False).order_by('-start_time')[:5]

    is_member = group.members.filter(id=request.user.id).exists()
    is_admin = is_member and GroupMembership.objects.filter(user=request.user, group=group, role='admin').exists()
    resource_form = GroupResourceForm()

    context = {
        'group': group,
        'chat_messages': group.chat_messages.all(),
        'past_sessions': past_group_sessions,
        'user_study_history': user_study_history,
        'active_session': active_session,
        'has_active_session': active_session is not None,
        'is_member': is_member,
        'is_admin': is_admin,
        'resource_form': resource_form,
    }
    return render(request, 'groups/group_detail.html', context)

@login_required
def upload_resource(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    if request.method == 'POST':
        form = GroupResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.group = group
            resource.uploaded_by = request.user
            resource.save()
            messages.success(request, 'Resource uploaded successfully.')
    return redirect('groups:group_detail', group_id=group.id)


@login_required
def join_group(request, invite_code):
    group = get_object_or_404(StudyGroup, invite_code=invite_code)
    if not group.members.filter(id=request.user.id).exists():
        GroupMembership.objects.create(user=request.user, group=group)
        messages.success(request, f"You have successfully joined the group '{group.name}'.")
    else:
        messages.info(request, f"You are already a member of the group '{group.name}'.")
    return redirect('groups:group_detail', group_id=group.id)