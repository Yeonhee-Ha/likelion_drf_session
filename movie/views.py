from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['GET', 'POST'])
def movie_list_create(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many = True)
        return Response(data = serializer.data)
    
    if request.method == 'POST':
        serializer = MovieSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            movie = serializer.save()
            content = request.data['content']
            tags = [words[1:] for words in content.split(' ') if words.startswith('#')]
            for t in tags:
                try:
                    tag = get_object_or_404(Tag, name =t)
                except:
                    tag = Tag(name = t)
                    tag.save()
                movie.tags.add(tag)
            movie.save()
            
            return Response(data = MovieSerializer(movie).data)
    
    
@api_view(['GET', 'PATCH', 'DELETE'])
def movie_detail_update_delete(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = MovieSerializer(instance=movie, data=request.data, partial=True)
        if serializer.is_valid():
            movie = serializer.save()
            movie.tags.clear()
            content = request.data.get("content")
            tags = [words[1:] for words in content.split(' ') if words.startswith('#')]
            for t in tags:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                movie.tags.add(tag)  # ← 필드명도 반드시 .tags 로!
            movie.save()

        return Response(data=MovieSerializer(movie).data)
            
    elif request.method == 'DELETE':
        movie.delete()
        data = {
            'deleted_movie': movie_id
        }
        return Response(data)



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