from django.contrib import admin
from .models import Post, Tag, Comments, Subscribe, Profile, WebsiteMeta


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comments)
admin.site.register(Subscribe)
admin.site.register(Profile)
admin.site.register(WebsiteMeta)
