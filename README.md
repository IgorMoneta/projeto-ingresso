🎟️ Sistema de Ingressos – Django + HTML

     Sistema simples de venda e gestão de ingressos com área do cliente e painel administrativo, feito em Django REST Framework e HTML + JavaScript.

🚀 Funcionalidades]

👤 Cliente
Cadastro e login com CPF/
Listagem de eventos e ingressos/
Compra e confirmação de pagamento via PIX (simulado)

🛠 Admin
Login separado/
Gerenciamento de eventos, ingressos e bloqueios de CPF

⚙️ Tecnologias

Backend: Django + Django REST Framework + SimpleJWT

Frontend: HTML, CSS e JavaScript (Fetch API)

Autenticação: JWT

CORS: django-cors-headers

🧩 Como Rodar

1️⃣ Backend

cd backend

pip install -r requirements.txt

python manage.py makemigrations 

python manage.py makemigrations ingresso

python manage.py createsuperuser

python manage.py migrate

python manage.py runserver

2️⃣ Frontend

cd frontend

python -m http.server 5500

3️⃣ Acesse

👤 Cliente: http://localhost:5500/cliente_login.html

🛠 Admin: http://localhost:5500/admin_login.html


