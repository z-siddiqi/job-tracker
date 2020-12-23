from django.views.generic.edit import BaseCreateView, BaseUpdateView, BaseDeleteView
from django.utils.decorators import method_decorator

from utils.mixins import ajax_required, JsonResponseMixin, AjaxFormMixin


class BaseAjaxView(JsonResponseMixin):
    @method_decorator(ajax_required)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BaseAjaxEditView(AjaxFormMixin, BaseAjaxView):
    def get_success_data(self):
        url = self.get_success_url()
        return {"status": 302, "url": url}


class AjaxCreateView(BaseAjaxEditView, BaseCreateView):
    def form_valid(self, form):
        self.object = form.save()
        self.response_payload = self.get_success_data()
        return self.render_to_response({})


class AjaxUpdateView(BaseAjaxEditView, BaseUpdateView):
    def form_valid(self, form):
        self.object = form.save()
        self.response_payload = self.get_success_data()
        return self.render_to_response({})


class AjaxDeleteView(BaseAjaxEditView, BaseDeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        self.response_payload = self.get_success_data()
        return self.render_to_response({})
