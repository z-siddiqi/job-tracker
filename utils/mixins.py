from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse

from boards.models import Board, Job


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return redirect("home")
        return f(request, *args, **kwargs)

    return wrap


class UserAccessMixin:
    redirect_url = None

    def get_redirect_url(self):
        return self.redirect_url

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func()
        if not user_test_result:
            if request.is_ajax():
                return JsonResponse({}, status=403)
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)


class BoardPermissionMixin(UserAccessMixin):
    def get_board(self):
        return get_object_or_404(Board, slug=self.kwargs["board_slug"])

    def test_func(self):
        obj = self.get_board()
        return obj.user == self.request.user


class JobPermissionMixin(UserAccessMixin):
    def get_job(self):
        return get_object_or_404(Job, slug=self.kwargs["job_slug"])

    def test_func(self):
        obj = self.get_job()
        return obj.board.user == self.request.user


class FormInvalidStatus400Mixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response
