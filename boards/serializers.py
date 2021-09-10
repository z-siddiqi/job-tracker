from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    board_slug = serializers.CharField(source="board.slug")

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
        )
