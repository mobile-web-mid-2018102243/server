from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from . import models

from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from .serializers import PostSerializer
from .serializers import PostDetailSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status

class SignupView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):

        print(request.data['nickname'])
        print(request.data['id'])
        print(request.data['password'])
        user = User.objects.create_user(username=request.data['id'], password=request.data['password'])
        profile = models.Profile(user=user, nickname=request.data['nickname'])

        user.save()
        profile.save()

        return Response({"Sucess": True, "Result" : {}})

class SigninView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        user = authenticate(username=request.data['id'], password=request.data['password'])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"Success" : True, 'Result' : {'Token' : token.key}})
        else:
            return Response({"Success" : False, 'Result' : {}},status=401)

class GetPostListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        content = {
            'user': str(request.user),  # 인증된 사용자의 이름
            'auth': str(request.auth),  # 사용자와 연결된 토큰
        }

        print(content)
        serializer_class = PostSerializer
        posts = models.Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({"Success": True, 'Result': {"postList" : serializer.data}})


class GetMyPostListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        content = {
            'user': str(request.user),  # 인증된 사용자의 이름
            'auth': str(request.auth),  # 사용자와 연결된 토큰
        }

        serializer_class = PostSerializer
        user = User.objects.get(username=str(request.user))
        profile = models.Profile.objects.get(user = user)
        posts = models.Post.objects.filter(owner=profile)
        serializer = PostSerializer(posts, many=True)
        return Response({"Success": True, 'Result': {"postList" : serializer.data}})

class SolvePost(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,pk):
        content = {
            'user': str(request.user),  # 인증된 사용자의 이름
            'auth': str(request.auth),  # 사용자와 연결된 토큰
        }

        serializer_class = PostDetailSerializer
        user = User.objects.get(username=str(request.user))
        profile = models.Profile.objects.get(user = user)
        posts = models.Post.objects.get(pk=pk)
        serializer = PostDetailSerializer(posts,context={'request': request})
        return Response({"Success": True, 'Result': {"postList" : serializer.data}})

    def patch(self,request,pk):
        post = get_object_or_404(models.Post, pk=pk)

        title = request.data['title']
        text = request.data['text']

        # 필드 값을 변경
        post.title = title
        post.text = text
        # 변경 사항 저장

        try:
            post.save()
            return Response({"Success": True, 'Result': {}})
        except Exception as e:
            return Response({"Success": False, 'Result': {'Error': str(e)}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,pk):
        post = get_object_or_404(models.Post, pk=pk)

        if str(post.owner.user) != str(request.user):
            return Response({"Success": False,'Result' : {'Error' : "다른 사람 포스트 삭제 불가"} }, status=status.HTTP_403_FORBIDDEN)

        try:
            post.delete()
            return Response({"Success": True, 'Result': {}})
        except Exception as e:
            return Response({"Success": False, 'Result': {'Error': str(e)}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)