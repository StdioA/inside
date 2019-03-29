from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


def api_login_required(func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "success": False,
                "reason": "Login required"
            }, status=401)
        return func(request, *args, **kwargs)

    return wrapped


def api_perm_required(perm):
    def decorator(func):
        def wrapped(self, request, *args, **kwargs):
            if not request.user.has_perm(perm):
                return JsonResponse({
                    "success": False,
                    "reason": "Permission denied"
                }, status=403)
            return func(self, request, *args, **kwargs)

        return wrapped
    return decorator


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "success": False,
                "reason": "Login required"
            }, status=401)

        permission_dict = getattr(self, "permission_dict", {})
        permission = permission_dict.get(request.method.lower())
        if permission and not request.user.has_perm(permission):
            return JsonResponse({
                "success": False,
                "reason": "Permission denied"
            }, status=403)

        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return JsonResponse({
                "success": False,
                "reason": "Object does not exist"
            }, status=404)
