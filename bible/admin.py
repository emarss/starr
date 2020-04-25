from django.contrib import admin
from .models import Bible, BibleNotebook, BibleComment, BibleHistory, BibleBookmark

# Register your models here.
admin.site.register(Bible)
admin.site.register(BibleNotebook)
admin.site.register(BibleComment)
admin.site.register(BibleHistory)
admin.site.register(BibleBookmark)