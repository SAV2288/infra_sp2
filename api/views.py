from rest_framework import viewsets, permissions
from rest_framework import mixins
from rest_framework import filters
from rest_framework import exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from pytils import translit

from api.models import Titles
from api.models import Genres
from api.models import Categories
from api.models import Review
from api.models import Comment
from api.models import Rate
from api.serializers import GenreSerialiser
from api.serializers import CategorySerializer
from api.serializers import TitleSerializer
from api.serializers import ReviewSerializer
from api.serializers import CommentSerializer
from users.permissions import IsAccountAdminOrReadOnly, IsOwnerOrReadOnly, AuthorizedPermission


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AuthorizedPermission,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):

        score_value = self.request.data.get('score')

        try:
            title = Titles.objects.get(pk=self.kwargs['title_id'])
        except Titles.DoesNotExist:
            raise exceptions.NotFound(f"Title with '{self.kwargs['title_id']}' id doesn't exist")

        if Review.objects.filter(title=title, author=self.request.user).exists():
            raise exceptions.ValidationError('You already made review')

        try:
            score = Rate.objects.get(title=title)

        except Exception:
            Rate.objects.create(title=title, rate=score_value, count=1)
        else:
            score.rate_update(score=float(score_value), new=True)

        serializer.save(author=self.request.user, title=title, score=score_value)

    def perform_update(self, serializer):
        score_value = self.request.data.get('score')

        try:
            title = Titles.objects.get(pk=self.kwargs['title_id'])

        except Exception:
            raise exceptions.NotFound(f"Title with '{self.kwargs['title_id']}' id doesn't exist")

        score = get_object_or_404(Rate, title=title)

        score.rate_update(score=float(score_value), new=False)

        serializer.save(author=self.request.user, title=title, score=score_value)

    def get_queryset(self):
        try:
            title = Titles.objects.get(pk=self.kwargs['title_id'])
        except Exception:
            raise exceptions.NotFound(f"Title with '{self.kwargs['title_id']}' id doesn't exist")

        return Review.objects.filter(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    pagination_class = PageNumberPagination

    permission_classes = [AuthorizedPermission,
                          IsOwnerOrReadOnly
                          ]

    def get_queryset(self):

        return Comment.objects.filter(review_id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):

        try:
            review = Review.objects.get(pk=self.kwargs.get('review_id'))
        except Review.DoesNotExist:
            raise exceptions.NotFound("Requested review doesn't exist")

        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = [IsAccountAdminOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def queryset_filter(self, queryset):
        params_name = {
            'name': 'name__contains',
            'genre': 'genre__slug',
            'category': 'category__slug',
            'year': 'year',
        }

        for param in self.request.query_params:
            if param in params_name:
                param_name = params_name[param]
                queryset = queryset.filter(
                    **{param_name: self.request.query_params.get(f'{param}')}
                )
        return queryset

    def get_queryset(self):
        queryset = Titles.objects.select_related('category').all().prefetch_related('genre', 'rating')
        if self.request.query_params:
            queryset = self.queryset_filter(queryset)

        return queryset

    def validate_data(self, data, param):
        if not data:
            raise ValidationError(f"'{param}': Invalid parameter value!")

    def get_related_parameters(self):
        result_data = {}
        model_dict = {
            'category': Categories,
            'genre': Genres,
        }

        for param in self.request.data:
            if param in model_dict:
                model = model_dict[param]
                data = model.objects.filter(
                    slug__in=self.request.data.getlist(f'{param}')
                )
                self.validate_data(data, param)
                if param == 'category':
                    result_data[param] = data[0]
                else:
                    result_data[param] = data
        return result_data

    def perform_create(self, serializer):
        result_data = self.get_related_parameters()
        serializer.save(**result_data)

    def perform_update(self, serializer):
        result_data = self.get_related_parameters()
        serializer.save(**result_data)


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet,
                   ):
    queryset = Genres.objects.all()
    serializer_class = GenreSerialiser
    permission_classes = [IsAccountAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']

    def perform_create(self, serializer):
        if not self.request.data.get('slug'):
            slug = translit.slugify(self.request.data.get('name'))
            serializer.save(slug=slug)
        serializer.save()


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet,
                      ):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAccountAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']

    def perform_create(self, serializer):
        if not self.request.data.get('slug'):
            slug = translit.slugify(self.request.data.get('name'))
            serializer.save(slug=slug)
        serializer.save()
