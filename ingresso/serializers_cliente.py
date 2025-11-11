from rest_framework import serializers
from .models import Evento, Ingresso, Pagamento

class EventoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ["id", "nome", "data", ]


class IngressoClienteSerializer(serializers.ModelSerializer):
    evento = EventoClienteSerializer(read_only=True)

    class Meta:
        model = Ingresso
        fields = ["id", "evento", "preco"]


class PagamentoClienteSerializer(serializers.ModelSerializer):
    ingresso = IngressoClienteSerializer(read_only=True)

    class Meta:
        model = Pagamento
        fields = ["id", "ingresso", "quantidade", "valor", "status", "data_pagamento"]


class CompraClienteSerializer(serializers.Serializer):
    ingresso_id = serializers.IntegerField()
    quantidade = serializers.IntegerField()
 