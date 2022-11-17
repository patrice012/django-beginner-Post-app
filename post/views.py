from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from .models import PostView, Author, Category, Post
from django.db.models import Count, Q
from django.contrib import messages


from .forms import PostForm, CommentForm
# Create your views here.

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None



def get_category_count():
    queryset = Post \
        .objects \
        .values('category__title') \
        .annotate(Count('category__title'))
    return queryset


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset,
        'query':query,
    }
    return render(request, 'post/search_result.html', context)




def index(request):

    post_count = Post.objects.all().count()
    post_featured = Post.objects.filter(featured = True)[:4]
    post_featured_count = post_featured.count()

    context = {'post_count':post_count,
              'post_featured':post_featured,
              'post_featured_count':post_featured_count}

    return render(request, 'post/index.html', context)


def post_list(request):
    post = Post.objects.all()
    context = {"post":post} 
    return render(request, 'post/post_list.html', context)


# def commentaire(request, id):
#     post = Post.objects.get(id=id)
#     user_comment = request.user
#     form_comment = CommentForm()
#     if request.method =='POST':
#         form_comment = CommentForm(request.POST)
#         if form_comment.is_valid():
#             form_comment.instance.user = user_comment
#             form_comment.instance.post = post
#             form_comment.save()
#             return redirect(reverse('post-detail', kwargs = {'id':post.pk}))
#             comment_count += post.comment_count
#             comment_view += post.view_count

#             print((comment_view))
    
#     context = {
#         'post':post,
#         'form_comment':form_comment,
#         'user_comment':user_comment,
#         'comment_count':comment_count,
#         'comment_view':comment_view,
#     }

#     return render(request, 'post/post_detail.html', context)




def post_detail(request, id):
    category_count = get_category_count()
    
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)
    create = post.timestamp
    modifi = post.mod_date
    # post_comment = post.comments.all().order_by('-timestamp')
    # print(post_comment)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))

    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form,

        'create':create,
        'modifi':modifi,
        # 'post_comment':post_comment,
    }
    return render(request, 'post/post_detail.html', context)




def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post/post_create.html", context)



def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post/post_create.html", context)




def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        messages.info(request, 'Le post'+ post.title + 'a été supprimer avec succés!')
        return redirect(reverse("post-list"))
    
    context = {
        'post':post,
        # 'form':form,
    }

    return render(request, 'post/post_delete.html', context)




