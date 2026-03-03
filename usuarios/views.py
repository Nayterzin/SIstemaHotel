from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Quarto, Reserva, Cliente, Funcionario
from .forms import CadastroClienteForm, ReservaForm, QuartoForm, FuncionarioForm

def pagina_opcoes(request):
    """Tela inicial: escolher login (funcionários) ou cadastro (cliente)."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        tipo_usuario = request.POST.get('tipo_usuario')
        if tipo_usuario == 'funcionario':
            return redirect('login')
        elif tipo_usuario == 'cliente':
            return redirect('cadastro')
    return render(request, 'usuarios/escolha.html')

def cadastro_usuario(request):
    """Cadastro de clientes (hóspedes)."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CadastroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso.')
            return redirect('login')
        else:
            messages.error(request, 'Erro no cadastro.')
    else:
        form = CadastroClienteForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

@login_required
def home(request):
    """Página inicial para funcionários."""
    return render(request, 'usuarios/home.html')

def logout_usuario(request):
    """Logout para funcionários."""
    auth_logout(request)
    return redirect('login')    

def login_usuario(request):
    """Login para todos os usuários."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'usuarios/login.html')

def home_F(request):
    """Página inicial para funcionários."""
    if request.user.is_authenticated:
        return render(request, 'usuarios/home.html')
    if request.method == 'GET':
        quartos = Quarto.objects.all()
        return render(request, 'usuarios/home.html', {'quartos': quartos})

def home_C(request):
    """Página inicial para clientes (hóspedes)."""
    if request.user.is_authenticated:
        return render(request, 'usuarios/home.html')
    if request.method == 'GET':
        quartos = Quarto.objects.filter(disponivel=True)
        return render(request, 'usuarios/home.html', {'quartos': quartos})

@login_required
def reservar_quarto(request, quarto_id):
    """Reservar um quarto."""
    quarto = Quarto.objects.get(id=quarto_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.quarto = quarto
            reserva.save()
            return redirect('home')
        else:
            messages.error(request, 'Erro na reserva.')
    else:
        form = ReservaForm()
    return render(request, 'usuarios/reserva.html', {'form': form})

def home_admin(request):
    """Página inicial para administradores."""
    if request.user.is_authenticated:
        return render(request, 'usuarios/home_admin.html')
    if request.method == 'GET':
        quartos = Quarto.objects.all()
        return render(request, 'usuarios/home_admin.html', {'quartos': quartos})

def editar_quarto(request, quarto_id):
    """Editar um quarto."""
    quarto = Quarto.objects.get(id=quarto_id)
    if request.method == 'POST':
        form = QuartoForm(request.POST, instance=quarto)
        if form.is_valid():
            form.save()
            return redirect('home_admin')
        else:
            messages.error(request, 'Erro na edição.')
    else:
        form = QuartoForm(instance=quarto)
    return render(request, 'usuarios/editar_quarto.html', {'form': form})

def adicionar_quarto(request):
    """Adicionar um quarto."""
    if request.method == 'POST':
        form = QuartoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_admin')
        else:
            messages.error(request, 'Erro na adição.')
    else:
        form = QuartoForm()
    return render(request, 'usuarios/adicionar_quarto.html', {'form': form})

def remover_quarto(request, quarto_id):
    """Remover um quarto."""
    quarto = Quarto.objects.get(id=quarto_id)
    if request.method == 'POST':
        quarto.delete()
        return redirect('home_admin')
    return render(request, 'usuarios/remover_quarto.html', {'quarto': quarto})

def remover_reserva(request, reserva_id):
    """Remover uma reserva."""
    reserva = Reserva.objects.get(id=reserva_id)
    if request.method == 'POST':
        reserva.delete()
        return redirect('home_admin')
    return render(request, 'usuarios/remover_reserva.html', {'reserva': reserva})

def editar_reserva(request, reserva_id):
    """Editar uma reserva."""
    reserva = Reserva.objects.get(id=reserva_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('home_admin')
        else:
            messages.error(request, 'Erro na edição.')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'usuarios/editar_reserva.html', {'form': form})
    
def adicionar_funcionario(request):
    """Adicionar um funcionário."""
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_admin')
        else:
            messages.error(request, 'Erro na adição.')
    else:
        form = FuncionarioForm()
    return render(request, 'usuarios/adicionar_funcionario.html', {'form': form})
