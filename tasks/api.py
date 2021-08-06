from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import DestroyModelMixin

from .models import Task
from .permissions import IsOwner


class TaskDetailView(DestroyModelMixin, GenericAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def toggle_task_completed(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed = not task.completed  # toggle the boolean field
        task.save()
        return Response(status=HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        return self.toggle_task_completed(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
