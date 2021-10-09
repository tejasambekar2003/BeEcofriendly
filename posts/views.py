from django.shortcuts import render
from .models import Post1, Like
from .forms import CreatePostForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from .helpers import get_post
from posts.helpers import get_posts


class CreatePostView(
        generic.CreateView
):
    model = Post1
    form_class = CreatePostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(CreatePostView, self).form_valid(form)
        # return render(request, 'posts/post.html') 

class DetailPostView(
        generic.DetailView
):
    model = Post1
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(DetailPostView, self).get_context_data(**kwargs)
        context['post'] = get_post(self.kwargs['slug'])

        return context

class AllPostsView(generic.ListView):
    model = Post1
    template_name = 'posts/postsAll.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return get_posts(self.request.user, wall=True)


@login_required
def like_post_view(request, *args, **kwargs):
    try:
        post = Post1.objects.get(slug=kwargs['slug'])

        _, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            messages.warning(
                request,
                'You\'ve already liked the post.'
            )
    except Post1.DoesNotExist:
        messages.warning(
            request,
            'Post does not exist'
        )

    return HttpResponseRedirect(
        reverse_lazy(
            'posts:view',
            kwargs={'slug': kwargs['slug']}
        )
    )


@login_required
def unlike_post_view(request, *args, **kwargs):
    try:
        like = Like.objects.get(
            post__slug=kwargs['slug'],
            user=request.user
        )
    except Like.DoesNotExist:
        messages.warning(
            request,
            'You didn\'t like the post.'
        )
    else:
        like.delete()

    return HttpResponseRedirect(
        reverse_lazy(
            'posts:view',
            kwargs={'slug': kwargs['slug']}
        )
    )