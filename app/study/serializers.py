from rest_framework import serializers

from study.models import Lesson, LessonViewInfo # noqa


# class MyLessonViewInfoSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = LessonViewInfo
#         fields = ('status', 'view_time')


class MyLessonSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    view_time = serializers.IntegerField()
    # view_info = serializers.SerializerMethodField()

    # def get_view_info(self, obj):
    #     view_info = LessonViewInfo.objects.get(
    #         user=self.context['user_id'],
    #         lesson_id=obj.id
    #     )
    #     return MyLessonViewInfoSerializer(view_info).data

    class Meta:
        model = Lesson
        fields = ('title', 'status', 'view_time')


class MyLessonByProductSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    view_time = serializers.IntegerField()
    last_view_datetime = serializers.DateTimeField()
    # view_info = serializers.SerializerMethodField()

    # def get_view_info(self, obj):
    #     view_info = LessonViewInfo.objects.get(
    #         user=self.context['user_id'],
    #         lesson_id=obj.id
    #     )
    #     return MyLessonViewInfoSerializer(view_info).data

    class Meta:
        model = Lesson
        fields = ('title', 'status', 'view_time', 'last_view_datetime')
