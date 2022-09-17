from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from .tasks import new_post

@receiver(m2m_changed, sender=Post.category.through, dispatch_uid='notify_post_created_signal')
def notify_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        new_post.apply_async([instance.id], countdown=5)



