from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, decorators, get_user_model
from django.contrib import messages
from django import forms
from core.decorators import candidate_required
from core.utils import is_candidate
from .forms import CandidateSignupForm
from .models import Profile
from django.contrib.auth.models import User

# ---------- public landing ----------
#def home(request):
 #   return render(request, "index.html", {"year": date.today().year})
def home(request):
    form = CandidateSignupForm()
    return render(request, 'index.html', {'candidate_form': form})

def careers(request):
    return render(request, "careers.html")

def products(request):
    return render(request, "products.html")


# ---------- login ----------    
#new changes
class LoginForm(forms.Form):
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role     = forms.CharField(widget=forms.HiddenInput)   # 'candidates' | 'companies'

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data["role"]
            email = form.cleaned_data["email"].lower()
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password, role=role)

            if user:
                login(request, user)
                request.session["role"] = role  # remember the role
                return redirect("dashboard")    # ⬅️ you must define 'dashboard' in urls.py
            else:
                messages.error(request, "Invalid credentials for that role.")
        else:
            messages.error(request, "Please correct the login form.")
        return redirect("home")
    return redirect("home")

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

#----- candidate signup---------
def candidate_signup_view(request):
    if request.method == 'POST':
        form = CandidateSignupForm(request.POST, request.FILES)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirmpassword = form.cleaned_data['confirmpassword']
            resume_file = request.FILES['resume']

            if password != confirmpassword:
                messages.error(request, "Passwords do not match.")
                return render(request, 'index.html', {'candidate_form': form})

            if User.objects.filter(username=email).exists():
                messages.error(request, "User with this email already exists.")
                return render(request, 'candidate_signup.html', {'candidate_form': form})

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname
            )

            profile = Profile.objects.create(user=user, resume=resume_file)
            profile.save()

            messages.success(request, "Candidate account created successfully. Please log in.")
            return redirect('dashboard')  # candidate dashboard URL name
    else:
        form = CandidateSignupForm()
    
    return render(request, 'candidate_signup.html', {'form': form})
#---------------------Company signup------------
def company_signup(request):
    return render(request, "company_signup.html")


