from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14)

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    TIPO_CARGO = [
        ('R', 'Recepcionista'),
        ('A', 'Administrador'),
        ('L', 'Limpeza'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=1, choices=TIPO_CARGO)


class Quarto(models.Model):
    QUARTO_TIPO = [
        ('S', 'Solteiro'),
        ('C', 'Casal'),
        ('F', 'Familia'),
    ]

    numero = models.CharField(max_length=10)
    tipo = models.CharField(max_length=1, choices=QUARTO_TIPO)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='quartos/', null=True, blank=True)

    def __str__(self):
        return f'Quarto {self.numero} - {self.get_tipo_display()}'


class Reserva(models.Model):
    STATUS_RESERVA = [
        ('P', 'Pendente'),
        ('C', 'Confirmada'),
        ('F', 'Finalizada'),
    ]

    STATUS_LIMPEZA = [
        ('L', 'Limpo'),
        ('N', 'Não limpo'),
    ]

    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE)
    data_check_in = models.DateField()
    data_check_out = models.DateField()
    valor_reserva = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_RESERVA, default='Pendente')
    data_reserva = models.DateTimeField(auto_now_add=True)
    status_limpeza = models.CharField(max_length=20, choices=STATUS_LIMPEZA, default='Não limpo')

    def __str__(self):
        return f'Reserva de {self.usuario.nome} para o quarto {self.quarto.numero} - Status: {self.get_status_display()}'

