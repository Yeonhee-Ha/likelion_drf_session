from django.shortcuts import render

import re

from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

from django.shortcuts import get_object_or_404

# Create your views here.

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        return MovieSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        
        movie = serializer.instance
        self.handle_tags(movie)
        
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        movie = serializer.save()
        movie.tags.clear()
        self.handle_tags(movie)
        
    def handle_tags(self, movie):
        words = re.split(r'[\s,]+', movie.content.strip())
        tag_list = []
        
        for w in words:
            if len(w) > 0:
                if w[0] == '#':
                    tag_list.append(w[1:])
        for t in tag_list:
            tag, _ = Tag.objects.get_or_create(name=t)
            movie.tags.add(tag)
        movie.save()


    



@api_view(['GET', 'POST'])
def comment_read_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'GET':
        comments = Comment.objects.filter(movie = movie)
        serializer = CommentSerializer(comments, many = True)
        return Response(data=serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(movie=movie)
        return Response(serializer.data)
    
    
    
#Tag 검색 구현을 위한 함수
@api_view(['GET'])
def find_tag(request, tags_name):
    tags = get_object_or_404(Tag, name = tags_name)
    if request.method == 'GET':
        movie = Movie.objects.filter(tags__in = [tags])
        serializers= MovieSerializer(movie, many = True)
        return Response(data = serializers.data)
    

class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    

class MovieCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    #queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        movie = self.kwargs.get("movie_id")
        queryset = Comment.objects.filter(movie_id = movie)
        return queryset
    
    #def list(self, request, movie_id = None):
    #    movie = get_object_or_404(Movie, id = movie_id)
    #    queryset = self.filter_queryset(self.get_queryset().filter(movie = movie))
    #    serializer = self.get_serializer(queryset, many=True)
    #    return Response(serializer.data)
    

    def create(self, request, movie_id = None):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(movie=movie)
        return Response(serializer.data)
    
    
    
class TagViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "name"
    lookup_url_kwarg = "tag_name"
    
    def retrieve(self, request, *args, **kwargs):
        tag_name = kwargs.get("tag_name")
        tags = get_object_or_404(Tag, name = tag_name)
        movies = Movie.objects.filter(tags = tags)
        serializer = MovieSerializer(movies, many = True)
        return Response(serializer.data)