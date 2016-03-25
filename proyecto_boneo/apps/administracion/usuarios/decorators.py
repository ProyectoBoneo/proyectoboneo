from django.http import HttpResponseForbidden
from django.utils.decorators import available_attrs
from django.utils.six import wraps

__author__ = 'rmotteta'

def user_is_profesor(view_func):
   @wraps(view_func, assigned=available_attrs(view_func))
   def _wrapped_view(request, *args, **kwargs):
       if request.user.is_profesor:
           return view_func(request, *args, **kwargs)
       else:
           return HttpResponseForbidden()
   return _wrapped_view

def user_is_alumno(view_func):
   @wraps(view_func, assigned=available_attrs(view_func))
   def _wrapped_view(request, *args, **kwargs):
       if request.user.is_alumno:
           return view_func(request, *args, **kwargs)
       else:
           return HttpResponseForbidden()
   return _wrapped_view

def user_is_staff(view_func):
   @wraps(view_func, assigned=available_attrs(view_func))
   def _wrapped_view(request, *args, **kwargs):
       if request.user.is_staff:
           return view_func(request, *args, **kwargs)
       else:
           return HttpResponseForbidden()
   return _wrapped_view

def user_is_not_alumno(view_func):
   @wraps(view_func, assigned=available_attrs(view_func))
   def _wrapped_view(request, *args, **kwargs):
       if request.user.is_staff or request.user.is_profesor:
           return view_func(request, *args, **kwargs)
       else:
           return HttpResponseForbidden()
   return _wrapped_view