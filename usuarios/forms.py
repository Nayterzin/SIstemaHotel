from django import forms

from .models import Cliente


class CadastroClienteForm(forms.ModelForm):
    """Formulário de cadastro apenas para clientes."""

    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'cpf']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seu@email.com'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
        }