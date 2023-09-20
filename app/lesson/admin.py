from django.contrib import admin
from .models import UserLesson, UserProduct, Product, Lesson, ProductLesson


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )


@admin.register(UserProduct)
class UserProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'product'
    )


@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'lesson'
    )


class ProductLessonInline(admin.TabularInline):
    model = Lesson.product.through
    extra = 2


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title'
    )
    inlines = (
        ProductLessonInline,
    )


@admin.register(ProductLesson)
class ProductLessonAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'product',
        'lesson'
    )
