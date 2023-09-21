from django.db.models import Sum
from django.contrib.auth import get_user_model

from rest_framework import serializers

from lesson.models import UserLesson, Product, UserProduct

User = get_user_model()


class UserLessonSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserLesson
        fields = ('user', 'lesson', 'time', 'status', 'date_last',)


class ProductSerializer(serializers.ModelSerializer):
    count_full_lesson = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()
    count_users = serializers.SerializerMethodField()
    percent_add = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name', 'count_full_lesson',
            'total_time', 'count_users',
            'percent_add'
        )

    def get_count_full_lesson(self, obj):
        result = 0
        qs = obj.productlesson.values_list('lesson', flat=True)
        for lesson_name in qs:
            for lesson in UserLesson.objects.filter(lesson=lesson_name):
                if lesson.status == 'Просмотрено':
                    result += 1
        return result

    def get_total_time(self, obj):
        result = obj.productlesson.exclude(
            lesson__user__isnull=True
        ).aggregate(Sum('lesson__user__time')).get('lesson__user__time__sum')
        return result

    def get_count_users(self, obj):
        result = obj.productlesson.exclude(
            lesson__user__isnull=True
        ).values_list('lesson__user')
        return len(result)

    def get_percent_add(self, obj):
        count_users_product = len(UserProduct.objects.filter(product=obj))
        count_users_all = len(User.objects.all())
        return count_users_product / count_users_all
