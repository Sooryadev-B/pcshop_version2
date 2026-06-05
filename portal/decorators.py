from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def staff_required(view_func):
    @wraps(view_func)
    @login_required(login_url='portal:login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Admin access required.')
            return redirect('portal:login')
        return view_func(request, *args, **kwargs)
    return wrapper
