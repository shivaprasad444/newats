from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from core.utils import is_candidate

def candidate_required(view):
    @login_required
    def _wrapped(request, *args, **kwargs):
        if is_candidate(request):
            return view(request, *args, **kwargs)
        return redirect("dashboard")          # or raise 403
    return _wrapped
