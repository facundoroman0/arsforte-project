"""
Security decorators for ArsForte.

Provides:
- log_access: Decorador para logging de accesos y operaciones sensibles
"""

import logging
import functools

security_logger = logging.getLogger('security')


def get_client_ip(request):
    """Extract client IP from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def log_access(action):
    """
    Decorador para logging de accesos y operaciones sensibles.
    
    Usage:
        @log_access('transaction_created')
        def post(self, request):
            ...
    
    Args:
        action: Description of the action being performed
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(self_or_request, *args, **kwargs):
            # Handle both function-based views and class-based view methods
            # For CBV methods, first arg is self, second is request
            # For FBV, first arg is request
            if hasattr(self_or_request, 'META'):
                # It's a request object (function-based view)
                request = self_or_request
            else:
                # It's self (class-based view method)
                request = args[0] if args else None
            
            if request and hasattr(request, 'user'):
                user = request.user if request.user.is_authenticated else 'anonymous'
                ip = get_client_ip(request)
                
                security_logger.info(
                    f"{action} | User: {user} | IP: {ip} | "
                    f"Method: {request.method} | Path: {request.path}"
                )
            
            result = view_func(self_or_request, *args, **kwargs)
            
            if request and hasattr(request, 'path'):
                if hasattr(result, 'status_code'):
                    status = result.status_code
                    if status >= 400:
                        user = request.user if request.user.is_authenticated else 'anonymous'
                        security_logger.warning(
                            f"{action} - FAILED | User: {user} | Status: {status}"
                        )
            
            return result
        return wrapper
    return decorator


def log_security_event(event_type):
    """
    Decorador para logging de eventos de seguridad específicos.
    
    Usage:
        @log_security_event('login_failed')
        def post(self, request):
            ...
    
    Args:
        event_type: Type of security event
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            ip = get_client_ip(request)
            
            security_logger.warning(
                f"Security Event: {event_type} | IP: {ip} | "
                f"Path: {request.path}"
            )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator