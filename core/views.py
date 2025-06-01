from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, decorators, get_user_model
from django.contrib import messages
from django import forms
from datetime import date, timedelta, datetime
from core.decorators import candidate_required
from core.utils import is_candidate
from django.utils import timezone
from .forms import CandidateSignupForm, TimesheetForm, ContactForm
from .models import Profile, Job, Timesheets
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db.models import Q


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
#@decorators.login_required
def dashboard(request):
    query = request.GET.get("query", "")
    if query:
        jobs = Job.objects.filter(title__icontains=query)
    else:
        jobs = Job.objects.all()
    return render(request, "dashboard.html", {"jobs": jobs, "query": query})


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
                return render(request, 'index.html', {'candidate_form': form})
            print("error")
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
    
    return render(request, 'index.html', {'candidate_form': form})
#---------------------Company signup------------
def company_signup(request):
    return render(request, "company_signup.html")
#---------------- candidate job detail-------
def job_detail_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, "job_detail.html", {"job": job})

#------------- candidate job search----------
@decorators.login_required
def dashboard_view(request):
    query = request.GET.get("query", "")
    if query:
        jobs = Job.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(company__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        jobs = Job.objects.all()

    contact_form = ContactForm()


    return render(request, "dashboard.html", {
        "jobs": jobs,
        "query": query,
        #"contact_form": contact_form,
        
        
    })
#---------------Candidate Timesheet----------

def get_week_range(ref_date):
    start = ref_date - timedelta(days=ref_date.weekday())
    end = start + timedelta(days=6)
    return start, end
@decorators.login_required
def candidate_timesheet_view(request):
    today = date.today()
    selected_date_str = request.GET.get('selected_date', today.isoformat())
    selected_date = date.fromisoformat(selected_date_str)

    # Handle week navigation
    if 'week' in request.GET:
        if request.GET['week'] == 'prev':
            selected_date -= timedelta(weeks=1)
        elif request.GET['week'] == 'next':
            selected_date += timedelta(weeks=1)

    # Calculate the week range from selected_date
    week_start, week_end = get_week_range(selected_date)

    # Filter timesheet entries for the user and week
    entries = Timesheets.objects.filter(user=request.user, date__range=(week_start, week_end)).order_by('date')

    form = TimesheetForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user

            # Calculate hours automatically if not submitted
            start = datetime.combine(date.today(), instance.start_time)
            end = datetime.combine(date.today(), instance.end_time)
            duration = (end - start).total_seconds() / 3600
            instance.hours = round(duration, 2)

            if request.POST.get('action') == 'submit':
                instance.submitted = True

            instance.save()
            return redirect('candidate_timesheet')

    context = {
        'week_start': week_start,
        'week_end': week_end,
        'form': form,
        'entries': entries,
        'selected_date': selected_date
    }
    return render(request, 'timesheet.html', context)

#-------- Contact us -------------
def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Contact Us Form Submission"
            from_email = form.cleaned_data['email']
            message_body = (
                f"Name: {form.cleaned_data['name']}\n"
                f"Email: {form.cleaned_data['email']}\n"
                f"Message:\n{form.cleaned_data['message']}"
            )
            send_mail(subject, message_body, from_email, ['shiva660p@gmail.com'])
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect('dashboard')
        else:
            # Repopulate dashboard with jobs and the form with errors
            query = request.GET.get("query", "")
            jobs = Job.objects.filter(
                Q(title__icontains=query) |
                Q(location__icontains=query) |
                Q(company__icontains=query) |
                Q(description__icontains=query)
            ) if query else Job.objects.all()

            return render(request, "dashboard.html", {
                "jobs": jobs,
                "query": query,
                "contact_form": form,  # form with errors
            })
    else:
        return redirect('dashboard')