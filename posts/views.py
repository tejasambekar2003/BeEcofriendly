from django.shortcuts import render
from .models import Post1, Like
from users.models import Drive
from .forms import CreatePostForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .helpers import get_post
from posts.helpers import get_posts


class CreatePostView(
        generic.CreateView
):
    model = Post1
    form_class = CreatePostForm
    template_name = 'posts/post_form.html'
    context_object_name = 'drive'

    def get_context_data(self, **kwargs):
        context = super(CreatePostView, self).get_context_data(**kwargs)
        context['drive'] = get_post(self.kwargs['pk_drive'])

        return context

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

# class AllPostsView(generic.ListView):
#     model = Post1
#     template_name = 'posts/postsAll.html'
#     context_object_name = 'posts'

#     def get_queryset(self):
#         return get_posts(self.request.user, wall=True)

def drive_all_posts(request, pk_drive):
    drive =  Drive.objects.get(pk = pk_drive)
    posts = drive.posts.all()
    context = {'posts':posts, 'drive':drive}
    return render(request, 'posts/postsAll.html', context)

def drive_posts(request, pk_drive):
    drive =  Drive.objects.get(pk = pk_drive)
    context = {'drive' : drive}
    if request.method == 'POST':
        caption = request.POST['caption']
        image = request.FILES['imagepost']
        author = request.user

        post = Post1(drive = drive, author =author, photo = image, caption = caption)
        post.save()
        return redirect('drive_all_posts')
    return render(request, 'posts/trail.html', context)
    



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