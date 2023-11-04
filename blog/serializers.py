from .models import Post,Profile
from rest_framework import serializers

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname',)

class PostSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'created_date', 'published_date', 'image', 'owner')

class PostDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'created_date', 'published_date', 'image', 'owner', 'is_mine')

    def get_is_mine(self, obj):
        # self.context['request']는 view에서 serializer를 호출할 때 context로 전달되어야 합니다.
        request = self.context.get('request')
        if request:
            return str(obj.owner.user) == str(request.user)
        return False

    def get_owner(self, obj):
        return obj.owner.nickname