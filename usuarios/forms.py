from django import forms
from .models import Cliente, Reserva, Quarto, Funcionario

class CadastroClienteForm(forms.ModelForm):
    """Formulário de cadastro apenas para clientes."""

    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'cpf']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Seu nome completo', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seu@email.com', 'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000', 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00', 'class': 'form-control'}),
        }

    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Crie uma senha', 'class': 'form-control'}))
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha', 'class': 'form-control'}))

class ReservaForm(forms.ModelForm):
    """Formulário para realizar reservas."""
    class Meta:
        model = Reserva
        fields = ['data_check_in', 'data_check_out', 'quarto']
        widgets = {
            'data_check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'quarto': forms.Select(attrs={'class': 'form-control'}),
        }

class QuartoForm(forms.ModelForm):
    """Formulário para gerenciamento de quartos."""
    class Meta:
        model = Quarto
        fields = ['numero', 'tipo', 'preco', 'disponivel']
        widgets = {
            'numero': forms.TextInput(attrs={'placeholder': 'Número do quarto', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'placeholder': 'Preço do quarto', 'class': 'form-control'}),
            'disponivel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FuncionarioForm(forms.ModelForm):
    """Formulário para gerenciamento de funcionários."""
    class Meta:
        model = Funcionario
        fields = ['usuario', 'cargo']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
        }

class MudarSenhaForm(forms.Form):
    """Formulário para mudança de senha."""
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Seu email', 'class': 'form-control'}))
    senha_atual = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha atual', 'class': 'form-control'}))
    nova_senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nova senha', 'class': 'form-control'}))
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar senha', 'class': 'form-control'}))
