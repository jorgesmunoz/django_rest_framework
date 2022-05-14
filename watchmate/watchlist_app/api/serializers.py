from platform import platform
from rest_framework import serializers

from watchlist_app.models import (
    Review,
    WatchList,
    StreamPlatform
)


"""serializers.ModelSerializer"""


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)


class WatchListSerializer(serializers.ModelSerializer):

    # reviews = ReviewSerializer(many=True, read_only=True)

    # Serializer methodField. There must be a method call get_<name>
    # Attributes that are outside model fields
    # https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    len_name = serializers.SerializerMethodField()

    platform = serializers.StringRelatedField(source='platform.name')

    class Meta:
        model = WatchList
        fields = '__all__'
        # exclude = ['active']

    def create(self, validated_data):
        return super().create(validated_data)

    def get_len_name(self, object):
        return len(object.title)

    # Object level validations
    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError(
                "Film title and storyline should be different")
        else:
            return data

    # Field level validations
    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Title is too short!")
        return value


# class StreamPlatformSerializer(serializers.ModelSerializer):

#     watchlist = WatchListSerializer(many=True, read_only=True)

#     # Returns de __str__ method of the model
#     # watchlist = serializers.StringRelatedField(many=True)

#     # HyperlinkedRelatedField create a link for each object
#     # watchlist = serializers.HyperlinkedRelatedField(
#     #     many=True,
#     #     read_only=True,
#     #     view_name='movie-detail'
#     # )

#     class Meta:
#         model = StreamPlatform
#         fields = '__all__'


# HyperlinkedModelSerializer
class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):

    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'


"""serializers.Serailizer"""
# # Validator function
# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")
#     return value


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     # Object level validations
#     """
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError(
#                 "Film name and description should be different")
#         else:
#             return data
#     """

#     # Field level validations
#     """
#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short!")
#         return value
#     """
