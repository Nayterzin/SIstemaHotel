from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Quarto, Reserva, Cliente, Funcionario
from .forms import CadastroClienteForm, ReservaForm, QuartoForm, FuncionarioForm, MudarSenhaForm

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
            # Extrair dados do formulário
            nome = form.cleaned_data.get('nome')
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('senha')
            confirmar_senha = form.cleaned_data.get('confirmar_senha')

            if senha != confirmar_senha:
                messages.error(request, 'As senhas não coincidem.')
                return render(request, 'usuarios/cadastro.html', {'form': form})

            # Criar usuário no Django
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Este e-mail já está cadastrado.')
                return render(request, 'usuarios/cadastro.html', {'form': form})

            user = User.objects.create_user(username=email, email=email, password=senha)
            
            # Salvar o cliente e associar ao usuário
            cliente = form.save(commit=False)
            cliente.usuario = user
            cliente.save()

            messages.success(request, 'Cadastro realizado com sucesso. Faça login agora.')
            return redirect('login')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os campos.')
    else:
        form = CadastroClienteForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

@login_required
def home(request):
    """Página inicial com redirecionamento baseado no cargo ou tipo de usuário."""
    # Se for funcionário, verifica o cargo
    if hasattr(request.user, 'funcionario'):
        cargo = request.user.funcionario.cargo
        if cargo == 'A':
            return redirect('home_admin')
        elif cargo == 'L':
            return redirect('home_limpeza')
        else:
            return redirect('home_F') # Recepcionista ou padrão
    
    # Se for cliente ou usuário comum
    return redirect('home_C')

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
    """Página inicial para funcionários (Recepcionistas)."""
    quartos = Quarto.objects.all()
    return render(request, 'usuarios/home.html', {'quartos': quartos})

def home_C(request):
    """Página inicial para clientes (hóspedes)."""
    quartos = Quarto.objects.all() # Mostra todos, mas destaca disponibilidade no card
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

@login_required
def home_admin(request):
    """Página inicial para administradores com estatísticas."""
    quartos = Quarto.objects.all()
    quartos_disponiveis_count = Quarto.objects.filter(disponivel=True).count()
    reservas_ativas_count = Reserva.objects.filter(status='C').count()
    
    context = {
        'quartos': quartos,
        'quartos_disponiveis_count': quartos_disponiveis_count,
        'reservas_ativas_count': reservas_ativas_count,
    }
    return render(request, 'usuarios/home_admin.html', context)

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

def remover_funcionario(request, funcionario_id):
    """Remover um funcionário."""
    funcionario = Funcionario.objects.get(id=funcionario_id)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('home_admin')
    return render(request, 'usuarios/remover_funcionario.html', {'funcionario': funcionario})


def check_in(request, reserva_id):
    """Confirmar uma reserva."""
    reserva = Reserva.objects.filter(status='P')    
    if request.method == 'POST':
        reserva.status = 'C'
        reserva.save()
        return redirect('home_admin')
    return render(request, 'usuarios/confirmar_reserva.html', {'reserva': reserva})

def check_out(request, reserva_id):
    """Finalizar uma reserva."""
    reserva = Reserva.objects.filter(status='C')    
    if request.method == 'POST':
        reserva.status = 'F'
        reserva.status_limpeza = 'N'
        reserva.save()
        return redirect('home_admin')
    return render(request, 'usuarios/check_out.html', {'reserva': reserva})

def listar_reservas(request):
    """Listar todas as reservas."""
    if request.user.is_authenticated:
        return render(request, 'usuarios/listar_reservas.html')
    if request.method == 'GET':
        reservas = Reserva.objects.all()
        return render(request, 'usuarios/listar_reservas.html', {'reservas': reservas})
    
def listar_funcionarios(request):
    """Listar todos os funcionários."""
    if request.user.is_authenticated:
        return render(request, 'usuarios/listar_funcionarios.html')
    if request.method == 'GET':
        funcionarios = Funcionario.objects.all()
        return render(request, 'usuarios/listar_funcionarios.html', {'funcionarios': funcionarios})
    
def relatorio_reservas(request):
    """Gerar relatório de reservas."""
    if request.user.is_authenticated:
        return render(request, 'usuarios/relatorio_reservas.html')
    if request.method == 'GET':
        reservas = Reserva.objects.all()
        return render(request, 'usuarios/relatorio_reservas.html', {'reservas': reservas})

@login_required
def home_limpeza(request):
    """Página inicial para funcionários da limpeza."""
    # Mostra quartos que não estão limpos primeiro
    quartos = Quarto.objects.all().order_by('status_limpeza') 
    return render(request, 'usuarios/home_limpeza.html', {'quartos': quartos})

def limpar_quarto(request, quarto_id):
    """Limpar um quarto."""
    quarto = Quarto.objects.get(id=quarto_id)
    if request.method == 'POST':
        quarto.status_limpeza = 'L'
        quarto.save()
        return redirect('home_limpeza')
    return render(request, 'usuarios/limpar_quarto.html', {'quarto': quarto})

def mudar_senha(request):
    """Mudar a senha do usuário."""
    if request.method == 'POST':
        form = MudarSenhaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            senha_atual = form.cleaned_data.get('senha_atual')
            nova_senha = form.cleaned_data.get('nova_senha')
            confirmar_senha = form.cleaned_data.get('confirmar_senha')

            if nova_senha != confirmar_senha:
                messages.error(request, 'As novas senhas não coincidem.')
                return render(request, 'usuarios/mudar_senha.html', {'form': form})

            user = authenticate(request, username=email, password=senha_atual)
            if user is not None:
                user.set_password(nova_senha)
                user.save()
                login(request, user)  # Mantém o usuário logado após a troca
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('home')
            else:
                messages.error(request, 'E-mail ou senha atual incorretos.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = MudarSenhaForm()
    return render(request, 'usuarios/mudar_senha.html', {'form': form})

