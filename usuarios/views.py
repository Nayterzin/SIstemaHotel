from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import CadastroClienteForm


def pagina_opcoes(request):
    """Tela inicial: escolher login (funcionários) ou cadastro (cliente)."""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'usuarios/escolha.html')


def login_usuario(request):
    """Login para usuários do Django (funcionários: atendente/limpeza/gerente)."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email_ou_usuario = request.POST.get('email_ou_usuario', '').strip()
        senha = request.POST.get('senha', '')

        if not email_ou_usuario or not senha:
            messages.error(request, 'Preencha e-mail/usuário e senha.')
            return render(request, 'usuarios/login.html')

        user = None
        if '@' in email_ou_usuario:
            try:
                user_obj = User.objects.get(email=email_ou_usuario)
                user = authenticate(request, username=user_obj.username, password=senha)
            except User.DoesNotExist:
                user = None

        if user is None:
            user = authenticate(request, username=email_ou_usuario, password=senha)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.get_full_name() or user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'home')

        messages.error(request, 'E-mail/usuário ou senha incorretos. Tente novamente.')

    return render(request, 'usuarios/login.html')


def cadastro_usuario(request):
    """Cadastro apenas para clientes (hóspedes)."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CadastroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Agora você pode prosseguir.')
            return redirect('opcoes')
    else:
        form = CadastroClienteForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


@login_required(login_url='login')
def home(request):
    """Página/painel após login (funcionários)."""
    return render(request, 'usuarios/home.html')


def logout_usuario(request):
    """Encerra a sessão e volta para a tela de opções."""
    auth_logout(request)
    messages.success(request, 'Você saiu do sistema.')
    return redirect('opcoes')