from django.utils.timesince import timesince
from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    board_slug = serializers.CharField(source="board.slug")
    updated_at = serializers.SerializerMethodField()

    def get_updated_at(self, obj):
        return timesince(obj.updated_at).split(",")[0]

    class Meta:
        model = Job
        fields = (
            "board_slug",
            "slug",
            "company",
            "logo",
            "title",
            "deadline",
            "progress",
            "description",
            "updated_at",
        )
