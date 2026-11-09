from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
import re #validador
from django.core.validators import validate_email #validador de email
from django.core.exceptions import ValidationError #validador erro
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import Usuarios

# Create your views here.

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')

    elif request.method == 'POST': #aqui renderiza e manda para o inicio
        username = (request.POST.get('username') or '').strip()
        email = (request.POST.get('email') or '').strip()
        senha = request.POST.get('senha') or ''
        confirmar_senha = request.POST.get('confirmar_senha') or ''

        #VALIDAÇÃO CARACTER USERNAME

        if len(username) < 3: #conta quantos caracteres tem
            messages.add_message(
                request,
                constants.ERROR,
                'O username deve ter no mínimo 3 caracteres.'
            )
            return render(request, 'cadastro.html')

        if len(username) > 20: #impede que tenha mais que isso de caracteres
            messages.add_message(
                request,
                constants.ERROR,
                'O username deve ter no máximo 20 caracteres.'
            )
            return render(request, 'cadastro.html')

        #VALIDAÇÃO E-MAIL

        try:
            validate_email(email) #validador de email, verifica se email possuiu todas as credencias necessárias
        except ValidationError:
            messages.add_message(
                request,
                constants.ERROR,
                'Digite um e-mail válido.'
            )
            return render(request, 'cadastro.html')

        #VALIDAÇÃO SENHA

        if len(senha) < 9: #minimo de caracteres para a senha
            messages.add_message(
                request,
                constants.ERROR,
                'A senha deve ter no mínimo 9 caracteres.'
            )
            return render(request, 'cadastro.html')

        if len(senha) > 14: #máximo de caracteres pra a senha
            messages.add_message(
                request,
                constants.ERROR,
                'A senha deve ter no máximo 14 caracteres.'
            )
            return render(request, 'cadastro.html')

        if ' ' in senha: #verifica se possuiu espaço dentro da senha
            messages.add_message(
                request,
                constants.ERROR,
                'A senha não pode conter espaços.'
            )
            return render(request, 'cadastro.html')

        if not re.search(r'[A-Z]', senha): #verifica e procura por pelo menos uma letra maiuscula na senha
            messages.add_message(
                request,
                constants.ERROR,
                'A senha deve possuir pelo menos uma letra maiúscula.'
            )
            return render(request, 'cadastro.html')

        if not re.search(r'[a-z]', senha): #procura por pelo menos uma letra minuscula na senha
            messages.add_message(
                request,
                constants.ERROR,
                'A senha deve possuir pelo menos uma letra minúscula.'
            )
            return render(request, 'cadastro.html')

        if not re.search(r'[0-9]', senha): #faz a verificação se possuiu numeros
            messages.add_message(
                request,
                constants.ERROR,
                'A senha deve possuir pelo menos um número.'
            )
            return render(request, 'cadastro.html')

        if not re.search(r'[^A-Za-z0-9\s]', senha): #verifica caracteres especias dentro da senha
            messages.add_message(
                request,
                constants.ERROR,
                'A senha deve possuir pelo menos um caractere especial.'
            )
            return render(request, 'cadastro.html')

        if senha != confirmar_senha:
            messages.add_message(
                request,
                constants.ERROR,
                'As senhas não coincidem.'
            )
            return render(request, 'cadastro.html')

        if Usuarios.objects.filter(username=username).exists():
            messages.add_message(
                request,
                constants.ERROR,
                'Esse username já está cadastrado.'
            )
            return render(request, 'cadastro.html')

        if Usuarios.objects.filter(email=email).exists():
            messages.add_message(
                request,
                constants.ERROR,
                'Esse e-mail já está cadastrado.'
            )
            return render(request, 'cadastro.html')

        Usuarios.objects.create_user( #alteração de create para create_user para o sistema criar um hash de senha
            username=username,
            email=email,
            password=senha
        )

        messages.add_message(
            request,
            constants.SUCCESS,
            'Cadastro realizado com sucesso!'
        )

        return redirect('login')


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")

    username = (request.POST.get("username") or "").strip()
    senha = request.POST.get("senha") or ""

    user = authenticate( #troca de object.filter por authenticate, pois o primeiro realiza uma consulta no banco e o outro verifica se os dados estão corretos como a senha em hash e depois confirma para o django
    request,
    username=username,
    password=senha
    )

    if user is None:
        messages.add_message(
            request,
            constants.ERROR,
            "Username ou senha inválidos."
        )
        return redirect("login")

    login(request, user) #verifica que o usuarios está ou não ligado na sessão

    messages.add_message(
        request,
        constants.SUCCESS,
        "Login realizado com sucesso!"
    )

    return redirect("painel_teste")

@login_required #Decorators é uma verificação pontual se aquele usuario é permitido ou não a acessar aquela parte do sist. É o segurança que guarda uma sala
@login_required #Decorators é uma verificação pontual se aquele usuario é permitido ou não a acessar aquela parte do sist. É o segurança que guarda uma sala
def painel_teste(request):

    if request.method == 'POST':

        imagem = request.FILES.get('imagem')

        if imagem:

            request.user.imagem = imagem

            request.user.save()

            messages.add_message(
                request,
                constants.SUCCESS,
                'Imagem atualizada com sucesso!'
            )

        return redirect('painel_teste')

    return render(request, 'painel_teste.html')


def logout_view(request):

    logout(request)

    return redirect('login')

@login_required
@require_POST
def alternar_tema(request):
    try:
        dados = json.loads(request.body)
        modo_escuro = dados.get('modo_escuro')

        if not isinstance(modo_escuro, bool):
            return JsonResponse(
                {'erro': 'Valor de tema inválido.'},
                status=400
            )

        request.user.modo_escuro = modo_escuro
        request.user.save(update_fields=['modo_escuro'])

        return JsonResponse({
            'sucesso': True,
            'modo_escuro': request.user.modo_escuro
        })

    except (json.JSONDecodeError, TypeError):
        return JsonResponse(
            {'erro': 'Não foi possível atualizar o tema.'},
            status=400
        )

