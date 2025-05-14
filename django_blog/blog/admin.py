from django.contrib import admin
from blog import models
# Register your models here.
admin.site.register([models.UserProfile, models.Article, models.Comment,
                    models.ArticleLike, models.CommentLike])
