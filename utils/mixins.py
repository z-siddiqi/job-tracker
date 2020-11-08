from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


def ajax_required(f):

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return redirect('home')
        return f(request, *args, **kwargs)
    
    return wrap


class CustomLoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        return super().dispatch(request, *args, **kwargs)


class CustomUserPassesTestMixin(UserPassesTestMixin):

    def handle_no_permission(self):
        return redirect('home')