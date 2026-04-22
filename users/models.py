from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):

    email = models.EmailField(unique=True)
    notification_threshold = models.DecimalField(
        max_digits=5, decimal_places=2, default=50.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group, related_name='users_set',
        blank=True,
        help_text='Grupos a los que pertenece este usuario.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='users_user_set',
        blank=True,
        help_text='Persmisos específicos para este usuario.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
