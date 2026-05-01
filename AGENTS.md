# AGENTS.md - ArsForte Development Guide

## Build / Run Commands

### Development Server
```bash
cd ~/arsforte-project
source venv/bin/activate

# Start Redis (required for cache and rate limiting)
redis-server --daemonize yes

python manage.py runserver
```

### Redis Commands
```bash
# Start Redis
redis-server

# Check Redis is running
redis-cli ping  # Returns: PONG

# Clear all keys (cache/rate limit data)
redis-cli FLUSHALL

# View rate limit keys
redis-cli KEYS "rl:*"
```

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test transactions.tests

# Run specific test class
python manage.py test transactions.tests.TransactionTestCase

# Run specific test method
python manage.py test transactions.tests.TransactionTestCase.test_transaction_create
```

### Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Django Shell
```bash
python manage.py shell
```

---

## Security Features

### Security Headers (enabled by default)
- `SECURE_SSL_REDIRECT` - Redirect HTTP to HTTPS
- `SECURE_HSTS_SECONDS` - HSTS for 1 year
- `SECURE_CONTENT_TYPE_NOSNIFF` - Prevent MIME sniffing
- `SECURE_BROWSER_XSS_FILTER` - XSS protection
- `SECURE_REFERRER_POLICY` - Referrer policy

### Secure Cookies
- `SESSION_COOKIE_SECURE` - Secure cookies in production
- `SESSION_COOKIE_HTTPONLY` - Prevent JS access
- `SESSION_COOKIE_SAMESITE` - CSRF protection
- `SESSION_COOKIE_AGE` - 1 hour timeout

### Security Logging
- Logs to `security.log` file
- Records: user actions, IP addresses, request paths
- Location: `security/` module with `log_access` decorator

### Rate Limiting (django-ratelimit)
Rate limits applied to sensitive endpoints:

| Endpoint | Limit | Behavior |
|----------|-------|----------|
| POST /users/login/ | 5/min | Warning message |
| POST /users/register/ | 3/hour | HTTP 403 |
| POST /transactions/create/ | 20/min | HTTP 403 |
| POST /transactions/update/ | 20/min | HTTP 403 |
| POST /transactions/delete/ | 20/min | HTTP 403 |

Usage in views:
```python
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=False), name='post')
class LoginView(View):
    ...
```

---

## Code Style Guidelines

### General Principles
- Follow Django conventions and Django style guide
- Use Python 3.x type hints where beneficial
- Keep functions small and focused (single responsibility)
- Write docstrings for all public functions and classes

### Imports
```python
# Standard library
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

# Django
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

# Third party
from decouple import config

# Local apps
from services import bluelytics_service, coingecko_service
```

**Order:** Standard library → Django → Third party → Local apps

### Naming Conventions
- **Classes:** PascalCase (`Transaction`, `OpportunityCost`)
- **Functions/methods:** snake_case (`calculate_opportunity_cost`, `get_blue_rate`)
- **Constants:** UPPER_SNAKE_CASE (`DEFAULT_CACHE_TTL`)
- **Variables:** snake_case (`original_amount`, `user_id`)
- **Models:** Use `TextChoices` for choices, singular names (`Transaction` not `Transactions`)
- **URL names:** `app:name` format (`transactions:list`, `transactions:create`)

### Models
```python
class TransactionType(models.TextChoices):
    INCOME = 'income', 'Ingreso'
    EXPENSE = 'expense', 'Gasto'

class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices
    )
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-date']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.date}"
```

### Dataclasses (for data transfer objects)
```python
@dataclass
class OpportunityCost:
    """Represents opportunity cost analysis result."""
    original_amount: Decimal
    current_value: Decimal
    gain_loss: Decimal
    percentage: float
    instrument: str
    details: str
```

### Views
- Use function-based views (FBV) or class-based views appropriately
- Always require authentication with `@login_required` or `LoginRequiredMixin`
- Return appropriate HTTP status codes
- Use Django's messaging framework for user feedback

### Templates
- Use Django template tags and filters
- Keep logic in views, not templates
- Use template inheritance (`{% extends %}`)
- Include CSS/JS with `extra_css`/`extra_js` blocks per template
- Use CSS classes `.glass` for glassmorphism design

### Error Handling
- Use try/except for external API calls
- Implement graceful degradation for external services
- Log errors appropriately
- Return meaningful error messages to users

### Testing
- Test file naming: `tests.py` per app
- Test class naming: `TestCase` suffix (e.g., `TransactionTestCase`)
- Test method naming: `test_method_description`
- Use `setUp()` method for test fixtures
- Test both success and failure cases

### CSS/Design
- Global styles in `static/css/global-styles.css`
- Use CSS custom properties (variables) for colors
- Use `.glass` class for glassmorphism elements
- Badge variants: `.badge-glass-success`, `.badge-glass-danger`, `.badge-glass-warning`

### Django Best Practices
- Use `get_user_model()` for User model references
- Use `related_name` for reverse relationships
- Add database indexes for frequently queried fields
- Use `auto_now_add` for creation timestamps, `auto_now` for updates
- Separate concerns: models in `models.py`, forms in `forms.py`, views in `views.py`

---

## Project Structure

```
arsforte-project/
├── arsforte/              # Django project
│   ├── settings.py       # Project settings
│   ├── urls.py           # Root URLs
│   └── ...
├── users/                 # Users app
│   ├── models.py         # Custom User model
│   ├── views.py          # Auth views
│   └── tests.py
├── transactions/         # Transactions app
│   ├── models.py         # Transaction model
│   ├── views.py         # CRUD views
│   ├── forms.py         # Forms
│   └── tests.py
├── services/             # External API services
│   ├── bluelytics.py     # Dollar blue API
│   ├── coingecko.py      # Bitcoin API
│   ├── bcra.py           # UVA rates API
│   ├── inflation.py      # Inflation data
│   ├── cache.py          # Caching layer
│   └── opportunity_cost.py  # Cost calculations
├── security/             # Security module
│   ├── __init__.py
│   └── decorators.py     # @log_access decorator
├── templates/            # HTML templates
├── static/               # CSS, JS, images
│   └── css/
│       └── global-styles.css
├── docs/                 # Documentation
└── requirements.txt      # Dependencies
```

---

## Environment Variables
Create `.env` file with:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Redis Cache (optional - has defaults)
REDIS_URL=redis://localhost:6379/0
CACHE_KEY_PREFIX=arsforte

# Rate Limiting (optional - has defaults)
RATELIMIT_ENABLE=True
RATELIMIT_USE_CACHE=default
RATELIMIT_CACHE_PREFIX=rl:
```
