from django.db import models
from django.db.models.deletion import CASCADE
from users.models import Drive
from django.contrib.auth.models import User
from django.urls import reverse
import string as str
from random import choice

def generate_id():
    n = 10
    random = str.ascii_uppercase + str.ascii_lowercase + str.digits
    return ''.join(choice(random) for _ in range(n))

class Post1(models.Model):
    drive = models.ForeignKey(Drive, on_delete=CASCADE, null=True, related_name='posts')
    author = models.ForeignKey(User, related_name='post', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=10, default=generate_id)
    photo = models.FileField(upload_to='posts_photo')
    caption = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('posts:AllPostsView', kwargs={'pk_drive': self.pk})
# , kwargs={'slug': self.slug}
class Like(models.Model):
    post = models.ForeignKey(Post1, related_name='liked_post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='liker', on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.user, self.post)