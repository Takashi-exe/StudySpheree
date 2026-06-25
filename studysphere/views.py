from django.shortcuts import render

def root_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'admin_dashboard.html')
        else:
            friends = request.user.profile.friends.all()
            groups = request.user.study_groups.all()
            return render(request, 'dashboard.html', {'friends': friends, 'groups': groups})
    else:
        return render(request, 'landing.html')
