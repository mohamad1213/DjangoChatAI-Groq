import os
from django.shortcuts import render
from .models import AIResponse
from .forms import AIForm
from groq import Groq
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.utils.timezone import now
from .forms import RegisterForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('ai_page')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ai_page')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login berhasil!")
            return redirect("generate_ai")  # Redirect ke halaman setelah login
        else:
            messages.error(request, "Username atau password salah.")
    
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    messages.success(request, "Anda telah logout.")
    return redirect("login")
from dotenv import load_dotenv

load_dotenv()  # Memuat variabel dari .env

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
def dashboard(request):
    return render(request, 'index.html')
def get_trial_limit(request):
    trial_limit = 3  # Maksimal request gratis
    trial_session_key = "ai_trial_count"
    
    if trial_session_key not in request.session:
        request.session[trial_session_key] = 0
        request.session["trial_start"] = str(now().date())  # Simpan tanggal mulai trial

    trial_count = request.session[trial_session_key]

    # Periksa apakah trial masih berlaku (misalnya 3 hari)
    trial_start_date = datetime.datetime.strptime(request.session["trial_start"], "%Y-%m-%d").date()
    trial_days_limit = 3  # 3 hari free trial
    if (now().date() - trial_start_date).days > trial_days_limit:
        trial_count = trial_limit  # Paksa pengguna login setelah 3 hari

    return trial_count, trial_limit
def ai_view(request):
    response_text = ""
    trial_count, trial_limit = get_trial_limit(request)

    # Jika pengguna belum login dan sudah mencapai batas trial, arahkan ke login
    if not request.user.is_authenticated and trial_count >= trial_limit:
        return redirect("login")

    if request.method == "POST":
        form = AIForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                stream=False,
            )
            response_text = chat_completion.choices[0].message.content

            # Simpan hasil ke database jika pengguna login
            if request.user.is_authenticated:
                AIResponse.objects.create(user=request.user, prompt=prompt, response=response_text)
            else:
                request.session["ai_trial_count"] += 1  # Tambah hitungan trial

    else:
        form = AIForm()

    return render(request, "ai_page.html", {"form": form, "response": response_text, "trial_limit": trial_count >= trial_limit})

@login_required
def ai_generate(request):
    response_text = ""
    if request.method == 'POST':
        form = AIForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                stream=False,
            )
            response_text = chat_completion.choices[0].message.content
            AIResponse.objects.create(user=request.user,prompt=prompt, response=response_text)
    else:
        form = AIForm()
    return render(request, 'chat.html', {'form': form, 'response': response_text})
