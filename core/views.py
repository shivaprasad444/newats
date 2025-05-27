from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, decorators
from django.contrib import messages
from django import forms
from core.decorators import candidate_required
from core.utils import is_candidate

# ---------- public landing ----------
def home(request):
    return render(request, "index.html", {"year": date.today().year})

def careers(request):
    return render(request, "careers.html")

def products(request):
    return render(request, "products.html")


# ---------- login ----------
class LoginForm(forms.Form):
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role     = forms.CharField(widget=forms.HiddenInput)   # 'candidates' | 'companies'

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data["role"]
            print(role)
            user = authenticate(
                request,
                username=form.cleaned_data["email"].lower(),
                password=form.cleaned_data["password"],
                role=role,
            )
            print(user)
            if user:
                print("redirecting to dashboard")
                login(request, user)
                request.session["role"] = role           # <-- remember role
                return redirect("dashboard")
            messages.error(request, "Invalid credentials for that role.")
        return redirect("home")                           # back to modal
    return redirect("home")                               # GET → landing


def logout_view(request):
    logout(request)
    return redirect("home")


# ---------- protected area ----------
@decorators.login_required
def dashboard(request):
    return render(request, "dashboard.html")


# ---- candidate-only sections ----
@candidate_required
def profile(request):
    return render(request, "candidate/profile.html")

@candidate_required
def jobs_applied(request):
    return render(request, "candidate/jobs_applied.html")

@candidate_required
def interviews(request):
    return render(request, "candidate/interviews.html")

@candidate_required
def calendar(request):
    return render(request, "candidate/calendar.html")
