from django.contrib import admin

# Register your models here.
from blog.models import Account, Category, Type, Story, Label


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'password', 'is_admin', 'is_staff', 'is_superuser', 'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
