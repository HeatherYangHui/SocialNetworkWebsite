from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    # Each profile is associated with a unique user
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    
    # Bio field for user to add a description
    bio = models.CharField(max_length=200)
    
    # Profile picture upload functionality
    picture = models.FileField(blank=True)
    
    centent_type = models.CharField(blank=True, max_length=50)
    
    # # Many-to-Many relationship for following other users
    following = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"



# Data model for a todo-list item
class Post(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        """
        Meaningful string representation using the primary id and text.
        
        Returns:
        A meaningful description of an item object.
        """
        return f'id={self.id}, text="{self.text}"'   

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """Automatically create a Profile whenever a new User is saved."""
    if created:
        Profile.objects.create(user=instance)

# class Post(models.Model):
#     # Each post is linked to a user
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
#     # Content of the post
#     text = models.TextField()
    
#     # Timestamp of when the post was created
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Post by {self.user.username} at {self.created_at}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} on Post {self.post.id}"

