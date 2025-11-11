from django.db import models
from django.contrib.auth.models import AbstractUser

# Usuário com CPF
class Usuario(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.username


class Evento(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateTimeField()

    def __str__(self):
        return self.nome


class Ingresso(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    lote = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_total = models.IntegerField()
    quantidade_disponivel = models.IntegerField()

    def __str__(self):
        return f"{self.evento.nome} - Lote {self.lote}"


class BloqueioCPF(models.Model):
    cpf = models.CharField(max_length=14, unique=True)
    motivo = models.TextField(blank=True, null=True)
    data_bloqueio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CPF {self.cpf} BLOQUEADO"


class Pagamento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ingresso = models.ForeignKey(Ingresso, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    metodo = models.CharField(max_length=20, choices=[('PIX', 'PIX')], default='PIX')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pendente', 'pendente'), ('pago', 'pago')], default='pendente')
    pix_copia_cola = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pagamento {self.usuario.username} - {self.status}"
