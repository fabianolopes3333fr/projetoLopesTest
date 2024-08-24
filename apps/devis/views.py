from django.shortcuts import redirect, render
from apps.devis.forms import FormularioDetailForm

def devis(request):
    return render(request, "formulario_detail.html",)





