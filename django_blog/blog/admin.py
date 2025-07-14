from django.contrib import admin
from blog import models
# Register your models here.

admin.site.register([models.CustomUser, models.UserProfile, models.Article, models.Comment, models.ArticleLike, models.CommentLike])
