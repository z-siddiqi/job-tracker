from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse

from boards.models import Board, Job
from tasks.models import Task


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
                self.response_payload = {"status": 403}  # permission denied
                return self.render_to_response({})
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)


class BoardPermissionMixin(UserAccessMixin):
    def get_board(self):
        return get_object_or_404(Board, slug=self.kwargs["board_slug"])

    def test_func(self):
        obj = self.get_board()
        return obj.user == self.request.user


class JsonResponseMixin:
    def render_to_response(self, context):
        payload = self.get_response_payload(context)
        return JsonResponse(payload)

    def get_response_payload(self, context):
        if context:
            return self.get_form_html(context)
        return self.response_payload


class AjaxFormMixin:
    template_name = None

    def get_form_html(self, context):
        form_html = render_to_string(
            template_name=self.template_name, context=context, request=self.request
        )
        return {"form": form_html}
