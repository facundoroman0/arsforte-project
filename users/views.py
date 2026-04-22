from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views import View
from django import forms
from decimal import Decimal
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

User = get_user_model()


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido {user.email}')
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Sesión cerrada correctamente')
        return redirect('login')


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente')
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})


class NotificationThresholdView(LoginRequiredMixin, View):
    template_name = 'settings.html'
    login_url = 'login'

    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        return render(request, self.template_name, {'user': user})

    def post(self, request):
        threshold = request.POST.get('notification_threshold')
        try:
            threshold_value = Decimal(threshold)
            if 10 <= threshold_value <= 90:
                request.user.notification_threshold = threshold_value
                request.user.save()
                messages.success(request, f'Configuración guardada. Umbral: {threshold_value}%')
            else:
                messages.error(request, 'El umbral debe estar entre 10% y 90%')
        except (ValueError, TypeError):
            messages.error(request, 'Valor de umbral inválido')
        
        return redirect('settings')
