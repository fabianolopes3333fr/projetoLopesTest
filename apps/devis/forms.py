from devis.models import Devis
from django import forms
from core import settings
from django.core.mail import send_mail
import random
import string
import re


class FormularioDetailForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = ('servico', 'descricao', 'foto', 'last_name', 'first_name', 'telefone', 'disponibilidade', 'endereco', 'codpostal', 'vila','data_criacao')  # campos do formulário
        
        labels = {
            'servico': 'Type de prestation',
            'descricao': 'Détail du projet', 
            'foto': 'Photos du chantier',
            'last_name': 'Votre nom', 
            'first_name': 'Votre prenom', 
            'telefone': 'Votre portable', 
            'disponibilidade': 'Disponibilites', 
            'endereco': 'Adresse du projet', 
            'cod postal': 'Votre code postal', 
            'vila': 'Votre ville', 
            'data_criacao': 'Date de creation',
             
            
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FormularioDetailForm, self).__init__(*args, **kwargs)
        if self.user.is_authenticated:
            del self.fields['password1']
            del self.fields['password2']
        
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
        else:
            field.widget.attrs['class'] = 'form-control'
            
            
    def clean_devis_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
			
	# Verifique se a senha contém pelo menos uma letra maiúscula, uma letra minúscula e um caractere especial

        if not re.search(r'[A-Z]', password1) or not re.search(r'[a-z]', password1) or not re.search(r'[!@#$%^&*(),.?":{}|  <>]', password1):
            raise forms.ValidationError("Le mot de passe doit contenir \
			au moins 8 caractères, une majuscule, une lettre \
			minuscule et un caractère spécial.")
        return password1
    
    def clean_devis_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne sont pas les mêmes!")
        return password2
    
    def save(self, commit=True):
	    # Save the provided password in hashed format
        user = super().save(commit=False)
        if self.user.is_authenticated:
            password = ''.join(random.choices(string.digits, k=6)) # Gerar uma senha 
            user.set_password(password) # salvo essa senha
            user.force_change_password = True # força mudança de senha quando logar.
            send_mail( # Envia email para usuario
                'Votre mot de passe temporaire',
                f'Votre mot de passe temporaire pour accéder à la plateforme est: {password}',
                settings.DEFAULT_FROM_EMAIL, # De (em produção usar o e-mail que está no settings: settings.DEFAULT_FROM_EMAIL)
                [user.email], # para
                fail_silently=False,
            )
        else:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user