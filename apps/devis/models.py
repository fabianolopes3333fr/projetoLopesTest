from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid
from pages.models import Servico



class Devis(models.Model): 
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='devis')
    numero_fatura = models.CharField(max_length=50, default=uuid.uuid4)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    descricao = models.TextField(max_length=200, blank=True)
    foto = models.ImageField(upload_to='devis/foto/', blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    telefone =  models.CharField(max_length=20, blank=True)
    disponibilidade = models.CharField(max_length=1000)
    endereco = models.CharField(max_length=20, blank=True)
    codpostal = models.CharField(max_length=20, blank=True)
    vila = models.CharField(max_length=20, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    
    
    
    
    def __str__(self):
        return f' Devis: {self.usuario.email}'

    class Meta:
        verbose_name = "Devis"
        verbose_name_plural = "Devis"