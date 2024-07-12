import re
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from forum import models
from base.utils import add_form_errors_to_messages, filtrar_modelo
from django.shortcuts import get_object_or_404, render, redirect
from forum.forms import  PostagemForumComentarioForm, PostagemForumForm
from django.contrib import messages  

# listas de postagem
def lista_postagem_forum(request):
    form_dict = {}
    filtros = {}
    
    valor_busca = request.GET.get("titulo") # filtro de pesquisa no imput pesquisar
    if valor_busca:
        filtros["titulo"] = valor_busca
        filtros["descricao"] = valor_busca
        
    if request.path == '/forum/':
        postagens = models.PostagemForum.objects.filter(ativo=True)
        template_view = 'lista-postagem-forum.html'
    else:
        user = request.user
        template_view = 'dashboard/dash-lista-postagem-forum.html'
        if ['administrador', 'colaborador'] in user.groups.all() or user.is_superuser:
            postagens = models.PostagemForum.objects.filter(ativo=True)
        else:
            postagens = models.PostagemForum.objects.filter(usuario=user)
    
    postagens = filtrar_modelo(postagens, **filtros) 
       
    for el in postagens:
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form 
        
    # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3) # '3' é numero de registro por pagina
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    
    context = {'page_obj': page_obj, 'form_dict': form_dict}
    return render(request, template_view, context)

# formulario de criacao de postagens
@login_required
def criar_postagem_forum(request):
    form = PostagemForumForm()
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, request.FILES)
        if form.is_valid():
            postagem_imagens = request.FILES.getlist('postagem_imagens') # pega as imagens
            if len(postagem_imagens) > 5: # faz um count
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
            else:
                forum = form.save(commit=False)
                forum.usuario = request.user
                forum.save()
                for f in postagem_imagens:models.PostagemForumImagem.objects.create(postagem=forum, imagem=f)
                # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
                messages.success(request, 'Seu Post foi cadastrado com sucesso!')
                return redirect('lista-postagem-forum')
        else:
            add_form_errors_to_messages(request, form)
    return render(request, 'form-postagem-forum.html', {'form': form})

# visualizacao de postagem (slug)
def detalhe_postagem_forum(request, slug):
    postagem = get_object_or_404(models.PostagemForum, slug=slug)
    form = PostagemForumForm(instance=postagem)
    form_comentario = PostagemForumComentarioForm()
    context = {
        'postagem': postagem, 
        'form': form,
        'form_comentario':form_comentario
               
        }
    return render(request, 'detalhe-postagem-forum.html', context)

# Edita Postagem (slug)
@login_required
def editar_postagem_forum(request, slug):
    redirect_route = request.POST.get('redirect_route', '') # Adiciona
    postagem = get_object_or_404(models.PostagemForum, slug=slug)
    message = 'Seu Post '+ postagem.titulo +' foi atualizado com sucesso!'
    
    
    # Verifica se o usuário autenticado é o autor da postagem
    lista_grupos = ['administrador', 'colaborador']
    if request.user != postagem.usuario and not (
            any(grupo.name in lista_grupos for grupo in request.user.groups.all()) or request.user.is_superuser):
        messages.warning(request, 'Seu usuário não tem permissão para acessar esta pagina. ')
    # Redireciona para uma página de erro ou outra página adequada
        return redirect('lista-postagem-forum')  
    
    if request.method == 'POST':
        form = PostagemForumForm(request.POST, instance=postagem)
        if form.is_valid():
            contar_imagens = postagem.postagem_imagens.count() # Quantidade de imagens sque já tenho no post
            postagem_imagens = request.FILES.getlist('postagem_imagens') # Quantidade de imagens que estou enviando para salvar
            if contar_imagens + len(postagem_imagens) > 5:
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
                return redirect(redirect_route)
            else: 
                form.save()
                for f in postagem_imagens: # for para pegar as imagens e salvar.
                    models.PostagemForumImagem.objects.create(postagem=postagem, imagem=f)
                    
                messages.warning(request,message)
                return redirect(redirect_route)
        else:
            add_form_errors_to_messages(request, form)
    return JsonResponse({'status': message}) # Coloca por enquanto.

# deletar postagem
@login_required 
def deletar_postagem_forum(request, slug): 
    redirect_route = request.POST.get('redirect_route', '') # adiciono saber a rota que estamos
    print(redirect_route)
    postagem = get_object_or_404(models.PostagemForum, slug=slug)
    message = 'Seu Post '+postagem.titulo+' foi deletado com sucesso!' # atualizei a mesnagem aqui
    if request.method == 'POST':
        postagem.delete()
        messages.error(request, message)
        
        if re.search(r'/forum/detalhe-postagem-forum/([^/]+)/', redirect_route): # se minha rota conter
            return redirect('lista-postagem-forum')
        return redirect(redirect_route)

    return JsonResponse({'status':message})
    # return render(request, 'detalhe-postagem-form.html', {'postagem': postagem})
    
    
    # ajax para remover imagens 
def remover_imagem(request):
    imagem_id = request.GET.get('imagem_id') # Id da imagem
    verifica_imagem = models.PostagemForumImagem.objects.filter(id=imagem_id) # Filtra pra ver se imagem existe...
    if verifica_imagem:
        postagem_imagem = models.PostagemForumImagem.objects.get(id=imagem_id) # pega a imagem
        # Excluir a imagem do banco de dados e do sistema de arquivos (pasta postagem-forum/)
        postagem_imagem.imagem.delete()
        postagem_imagem.delete()
    return JsonResponse({'message': 'Imagem removida com sucesso.'})


""" 
    Funcoes refernte a comentarios 
"""
def adicionar_comentario(request, slug):
    postagem = get_object_or_404(models.PostagemForum, slug=slug)
    message = 'Comentário Adcionado com sucesso!'
    if request.method == 'POST':
        form = PostagemForumComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.postagem = postagem
            comentario.save() 
            messages.warning(request, message)
            return redirect('detalhe-postagem-forum', slug=postagem.slug)
    return JsonResponse({'status': message})

def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(models.PostagemForumComentario, id=comentario_id)
    message = 'Comentário Editado com sucesso!'
    if request.method == 'POST':
        form = PostagemForumComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.info(request, message)
            return redirect('detalhe-postagem-forum',
                            slug=comentario.postagem.slug)
    return JsonResponse({'status': message})

def deletar_comentario(request, comentario_id):
    comentario = get_object_or_404(models.PostagemForumComentario, id=comentario_id)
    comentario.delete()
    messages.success(request, 'Comentário deletado com sucesso!')
    return redirect('detalhe-postagem-forum', slug=comentario.postagem.slug)


def responder_comentario(request, comentario_id):
    comentario = get_object_or_404(models.PostagemForumComentario, id=comentario_id)
    if request.method == 'POST':
        form = PostagemForumComentarioForm(request.POST)
        message = 'Comentário Respondido com sucesso!'
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.usuario = request.user
            novo_comentario.parent_id = comentario_id
            novo_comentario.postagem = comentario.postagem
            novo_comentario.save()
            messages.info(request, message)
            return redirect('detalhe-postagem-forum',
                            slug=comentario.postagem.slug)
    return JsonResponse({'status': message})