from django.contrib import admin
from .models import AIResponse

class AIResponseAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'created_at', 'prompt_snippet')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'prompt', 'response')

    def get_username(self, obj):
        """Menampilkan username atau 'Anonymous' jika user null"""
        return obj.user.username if obj.user else "Anonymous"
    get_username.short_description = "User"

    def prompt_snippet(self, obj):
        """Menampilkan potongan kecil dari prompt untuk tampilan ringkas."""
        return obj.prompt[:50] + "..." if len(obj.prompt) > 50 else obj.prompt
    prompt_snippet.short_description = "Prompt"

admin.site.register(AIResponse, AIResponseAdmin)
