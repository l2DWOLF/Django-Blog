from django.db import models
from django.contrib.auth.models import User, AbstractUser
from taggit.managers import TaggableManager
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

# Custom User Model # 
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=True)

    def __str__(self):
        return self.username

# Users Profile Model #
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique = True)
    bio = models.TextField(max_length=500, blank=True, unique=True)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"
    
    @property
    def username(self):
        return self.user.username
    
# Articles Model #
STATUS_LIST = [
    ('draft', 'Draft'),
    ('publish', 'Publish'),
    ('archived', 'Archived')
]
class Article(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False,
        unique=True, validators=[
        MinLengthValidator(5), MaxLengthValidator(100),
        RegexValidator(regex = '^[a-zA-Z0-9].*$',
                        message="Title must start with a letter or number"),
        ],
        error_messages={
            'required': 'title is required',
            'blank': 'please enter a title',
        },
    )
    content = models.TextField(blank=False, null=False,
        unique=True, validators=[
        MinLengthValidator(15), MaxLengthValidator(4096)
        ],
        error_messages={
            'required': 'content is required',
            'blank': 'please enter content',
        },
    )
    status = models.CharField(max_length=10, choices=STATUS_LIST,
                                default='draft', error_messages={
                                    'required': 'status is required',
                                    'blank': 'please enter a status',
                                },
    )
    comments = []
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
# Comments Model # 
class Comment(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', null=True, blank=True,
                    default=None, on_delete=models.PROTECT)
    content = models.TextField(blank=False, null=False,
                validators=[MinLengthValidator(2), 
                            MaxLengthValidator(2048)
    ])
    status = models.CharField(max_length=10, choices=STATUS_LIST,
                            default='draft')
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"by: {self.author.username}, article - {self.article.pk}: {self.content} Reply TO: {self.reply_to}"

# Likes Models #
LIKE_STATUS = [
    ('like', 'Like'),
    ('dislike', 'Dislike')
]
# Articles Like Model #
class ArticleLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    status = models.CharField(max_length=7, 
                choices=LIKE_STATUS, default='like')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'article']

    def __str__(self):
        return f"{self.user.username} - {self.status} - {self.article.pk}"
    
# Comments Like Model # 
class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    status = models.CharField(max_length=7,
                choices=LIKE_STATUS, default='like')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [('user', 'comment')]

    def __str__(self):
        return f"{self.user.username} - {self.status}d - {self.comment.pk}"
