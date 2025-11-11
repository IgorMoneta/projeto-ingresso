import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions

from .models import Evento, Ingresso, Pagamento, BloqueioCPF
from .serializers_admin import EventoAdminSerializer, IngressoAdminSerializer, BloqueioAdminSerializer
from .serializers_cliente import EventoClienteSerializer, IngressoClienteSerializer, CompraClienteSerializer, PagamentoClienteSerializer


# ----- CLIENTE -----

class EventoListClienteView(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoClienteSerializer


class IngressoListClienteView(generics.ListAPIView):
    serializer_class = IngressoClienteSerializer

    def get_queryset(self):
        return Ingresso.objects.filter(evento_id=self.kwargs['evento_id'])


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comprar_ingresso(request):
    try:
        ingresso = Ingresso.objects.get(id=request.data['ingresso_id'])
    except Ingresso.DoesNotExist:
        return Response({"erro": "Ingresso não encontrado."}, status=404)

    usuario = request.user
    quantidade = int(request.data.get('quantidade', 1))

    if BloqueioCPF.objects.filter(cpf=usuario.cpf).exists():
        return Response({"erro": "Você está impedido de comprar ingressos."}, status=403)

    if ingresso.quantidade_disponivel < quantidade:
        return Response({"erro": "Ingressos insuficientes."}, status=400)

    valor_total = ingresso.preco * quantidade
    pix_code = f"PIX-{uuid.uuid4()}"

    pagamento = Pagamento.objects.create(
        usuario=usuario,
        ingresso=ingresso,
        quantidade=quantidade,
        valor=valor_total,
        pix_copia_cola=pix_code,
        status="pendente"
    )

    return Response({
        "mensagem": "PIX gerado. Pague para confirmar.",
        "pix_copia_cola": pix_code,
        "valor_total": float(valor_total),
        "pagamento_id": pagamento.id
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirmar_pagamento(request):
    pagamento = get_object_or_404(Pagamento, id=request.data['pagamento_id'], usuario=request.user)

    if pagamento.status == "pago":
        return Response({"mensagem": "Pagamento já confirmado."})

    ingresso = pagamento.ingresso

    if ingresso.quantidade_disponivel < pagamento.quantidade:
        return Response({"erro": "Ingressos esgotados."}, status=400)

    ingresso.quantidade_disponivel -= pagamento.quantidade
    ingresso.save()

    pagamento.status = "pago"
    pagamento.save()

    return Response({"mensagem": "Pagamento confirmado e ingresso garantido!"})


# ----- ADMIN -----

class EventoAdminView(generics.ListCreateAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoAdminSerializer
    permission_classes = [IsAdminUser]


class IngressoAdminView(generics.ListCreateAPIView):
    queryset = Ingresso.objects.all()
    serializer_class = IngressoAdminSerializer
    permission_classes = [IsAdminUser]


class BloqueioAdminView(generics.ListCreateAPIView):
    queryset = BloqueioCPF.objects.all()
    serializer_class = BloqueioAdminSerializer
    permission_classes = [IsAdminUser]

from django.contrib.auth.hashers import make_password
from .models import Usuario
from rest_framework import status

@api_view(['POST'])
def registrar_cliente(request):
    username = request.data.get('username')
    password = request.data.get('password')
    cpf = request.data.get('cpf')

    if not username or not password or not cpf:
        return Response({"erro": "Preencha todos os campos."}, status=status.HTTP_400_BAD_REQUEST)

    if Usuario.objects.filter(username=username).exists():
        return Response({"erro": "Usuário já existe."}, status=status.HTTP_400_BAD_REQUEST)

    if Usuario.objects.filter(cpf=cpf).exists():
        return Response({"erro": "CPF já cadastrado."}, status=status.HTTP_400_BAD_REQUEST)

    usuario = Usuario.objects.create(
        username=username,
        cpf=cpf,
        password=make_password(password)
    )

    return Response({"mensagem": "Usuário cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)
