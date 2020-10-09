from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.models import Genres, Rate
from api.models import Titles
from api.models import Categories
from api.models import Review
from api.models import Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ['id', 'author', 'text', 'pub_date']
        model = Comment


class GenreSerialiser(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False,
                                 validators=[UniqueValidator(queryset=Genres.objects.all())]
                                 )

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False,
                                 validators=[UniqueValidator(queryset=Categories.objects.all())]
                                 )

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerialiser(many=True, required=False, read_only=True)
    category = CategorySerializer(required=False, read_only=True)
    rating = serializers.IntegerField(source='rating.rate', read_only=True)

    class Meta:
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre', 'category']
        model = Titles
