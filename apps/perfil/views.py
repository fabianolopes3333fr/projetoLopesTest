from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from base.utils import filtrar_modelo
from forum.forms import PostagemForumForm
from contas.models import MyUser

def perfil_view(request, username):
    modelo = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(modelo, username=username)

    perfil_postagens = perfil.user_postagem_forum.all() # Todas as postagens relacionadas com perfil
    filtros = {} # Filtro dict

    valor_busca = request.GET.get("titulo") # Pego parametro
    if valor_busca:
        filtros["titulo"] = valor_busca # Adiciono no dicionario
        filtros["descricao"] = valor_busca
        
        # Utiliza o modelo das postagens do perfil
        perfil_postagens = filtrar_modelo(perfil_postagens, **filtros) # Faz o filtro
    
    
    
    form_dict = {}
    for el in perfil_postagens:
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form

     # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3)
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    context = {'obj': perfil, 'page_obj': page_obj, 'form_dict':form_dict}
    return render(request, 'perfil.html', context)
