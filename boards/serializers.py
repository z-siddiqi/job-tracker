from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    board_slug = serializers.SerializerMethodField()

    def get_board_slug(self, obj):
        return obj.board.slug

    class Meta:
        model = Job
        fields = (
            "board_slug",
            "slug",
            "company",
            "title",
            "deadline",
            "progress",
            "description",
        )
