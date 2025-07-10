from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'



class MovieSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)
    
    comments = serializers.SerializerMethodField(read_only = True)
    
    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many= True)
        return serializer.data
    
    
    #모델 내에서 굳이 안 만들어도 되는 변수 -> 시리얼라이저에서 사용하자
    tags = serializers.SerializerMethodField()
    
    #get_태그명 -> 이건 고정해야됨 ( 출력값 커스텀할 때 )
    def get_tags(self, instance):
        tag = instance.tags.all()
        return[t.name for t in tag]
    
    class Meta:
        model = Movie
        fields = '__all__'
    
    image = serializers.ImageField(use_url = True, required = False)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['movie']