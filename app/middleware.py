import datetime
from django.utils.timezone import now
from django.shortcuts import redirect

class TrialMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Jika pengguna sudah login, biarkan akses
        if request.user.is_authenticated:
            return self.get_response(request)

        # Cek apakah pengguna sudah memulai trial
        trial_start = request.session.get('trial_start')

        if not trial_start:
            # Jika belum ada trial, mulai trial hari ini
            request.session['trial_start'] = now().strftime('%Y-%m-%d')
        else:
            # Hitung selisih hari
            trial_start_date = datetime.datetime.strptime(trial_start, '%Y-%m-%d').date()
            days_passed = (now().date() - trial_start_date).days

            if days_passed > 3:
                return redirect('/login/')  # Paksa login setelah 3 hari

        return self.get_response(request)
