from rest_framework import serializers
from .models import Evento, Ingresso, BloqueioCPF

class EventoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = "__all__"

class IngressoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingresso
        fields = "__all__"

class BloqueioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloqueioCPF
        fields = "__all__"
