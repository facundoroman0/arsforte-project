from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django import forms
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()


class SettingsView(LoginRequiredMixin, View):
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
