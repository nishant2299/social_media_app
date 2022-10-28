from rest_framework.views import APIView
from rest_framework.response import Response
from social_media_app.models import FavoritePost, Post
from .serializers import UserSerializer, PostSerializer,ListPostSerializer, PostLikeSerializer,LoginUserSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class UserRegistration(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"user registered successfully","data":serializer.data,"status":201}, status=status.HTTP_201_CREATED)
        return Response({"msg":serializer.errors,"data":None,"status":400}, status=status.HTTP_400_BAD_REQUEST)




class LoginUserView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username, password=password)
            if user:
                token,created = Token.objects.get_or_create(user=user)
                print(type(token))
                data = {
                    "token": str(token),
                    "id":user.id,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "email":user.email
                }
                return Response({"msg":"success","data":data,"status":200}, status=status.HTTP_200_OK)
            return Response({"msg":"user not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePostView(APIView):
    def post(self,request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"msg":"post created successfully","data":serializer.data,"status":201}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListPostView(APIView):
    def get(self,request):
        post_object = Post.objects.all()
        serializer = ListPostSerializer(post_object, many=True)
        return Response({"data": serializer.data,"status":200})


class PostView(APIView):
    def get_object(self, pk):
        return Post.objects.get(pk=pk)
    
    def get(self, request, pk):
        try: 
            post_object = self.get_object(pk)
            serializer = ListPostSerializer(post_object)
            return Response({"data":serializer.data,"msg":"success"},status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"data":[],"msg":"post not found"})

    
    def patch(self, request, pk):
        try:
            post_object = self.get_object(pk)
            if post_object.user == request.user:
                serializer = PostSerializer(post_object, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data":serializer.data,"msg":"post updated successfully"})
                return Response({"msg":serializer.errors})
            return Response({"msg":"user not authorized","status":401},status=status.HTTP_401_UNAUTHORIZED)

        except ObjectDoesNotExist:
            return Response({"data":[],"msg":"post not found"})
    

    def delete(self, request, pk):
        try:
            post_object = self.get_object(pk)
            if post_object.user == request.user:
                post_object.delete()
                return Response({"msg":"post deleted successfully","status":202},status=status.HTTP_202_ACCEPTED)
            return Response({"msg":"user not authorized","status":401},status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({"msg":"post not found"})
    
            

class PostLikeView(APIView):
    def post(self,request):
        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            post_id = request.data['post']
            current_user = request.user
            fav_post_obj = FavoritePost.objects.filter(post=post_id,user=current_user).first()
            if fav_post_obj:
                fav_post_obj.delete()
                return Response({"msg":"post disliked successfully","status":202})
            serializer.save(user=current_user)
            return Response({"msg":"post liked successfully","status":201}, status=status.HTTP_201_CREATED)
        return Response({"msg":serializer.errors,"status":400}, status=status.HTTP_400_BAD_REQUEST)
