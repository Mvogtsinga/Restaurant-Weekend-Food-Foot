from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import MyUserCreationForm
from django.contrib.auth import logout
from .models import TableType, Reservation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.http import JsonResponse

@login_required(login_url='/login/') 
def index(request):
    return render(request, 'home')

def signup_view(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirigez vers la page que vous voulez après l'inscription
    else:
        form = MyUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect(reverse('admin:index'))  # Redirection vers la page d'administration
            return redirect('home')  # Redirection vers la page d'accueil après la connexion
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
        logout(request)
        return redirect('login')

@login_required
def account_delete(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('account_delete')
    return render(request, 'account_delete.html')

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def cancel_confirmation(request):
    return render(request, 'cancel_confirmation.html')

@login_required
def reserve_table(request):
    if request.method == 'POST':
        table_type_id = request.POST.get('table_type')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        duration = int(request.POST.get('duration', 2))  # Par défaut, 2 heures

        table_type = TableType.objects.get(id=table_type_id)

        # Convertir les chaînes de caractères en objets date et time
        reservation_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        reservation_time = datetime.strptime(time_str, "%H:%M").time()
        reservation_start = timezone.make_aware(datetime.combine(reservation_date, reservation_time))

        # Créez la réservation si la table est disponible
        try:
            reservation = Reservation(
                user=request.user,
                table_type=table_type,
                date=reservation_date,
                time=reservation_time,
                duration=timedelta(hours=duration)
            )
            reservation.save()
            messages.success(request, "Votre réservation a été effectuée avec succès.")
        except ValidationError as e:
            messages.error(request, e.message)
        return redirect('account')
    else:
        tables = TableType.objects.all()
        default_date = timezone.now().date().isoformat()
        return render(request, 'reserve_table.html', {'tables': tables, 'default_date': default_date})

@login_required
def account_view(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-date')
    return render(request, 'account.html', {'reservations': reservations})


def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        message = request.POST.get('message')

        # Préparer le contenu de l'email
        subject = f"Message de {first_name} {last_name}"
        email_message = f"Nom: {first_name} {last_name}\nEmail: {email}\nTéléphone: {contact_number}\n\nMessage:\n{message}"

        # Envoyer l'email
        send_mail(
            subject,
            email_message,
            settings.EMAIL_HOST_USER,
            ['mvogtsinga@gmail.com'],  # Email de réception
            fail_silently=False,
        )
        messages.success(request, "Votre message a été envoyé avec succès.")
        return redirect('contact')

    return render(request, 'contact.html')

def foods(request):
    return render(request, 'foods.html')

def about(request):
    return render(request, 'about.html')
