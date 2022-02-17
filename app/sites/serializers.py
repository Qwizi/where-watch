from rest_framework import serializers


class Process(serializers.Serializer):
    title_eng = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    poster = serializers.URLField()
    site_url = serializers.URLField(max_length=255)
    site_link = serializers.URLField(max_length=255)
