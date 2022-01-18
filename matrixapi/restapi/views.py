from django.shortcuts import render
from restapi.models import MyUser, Worknotes
from restapi.serializers import UserCreationSerializer, SigninSerializer, WorknotesSerializers
from rest_framework import mixins,generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class UserCreationView(generics.GenericAPIView,mixins.CreateModelMixin):
    model=MyUser
    serializer_class = UserCreationSerializer

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class SigninView(APIView):
    serializer_class=SigninSerializer

    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data["email"]
            password=serializer.validated_data["password"]
            user=authenticate(request,username=email,password=password)
            print(email,password)
            print(user)
            if user:
                login(request,user)
                token, create = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"INVALID USER"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)


class WorknotesAddView(generics.GenericAPIView,mixins.CreateModelMixin,
                  mixins.ListModelMixin):

    model=Worknotes
    serializer_class = WorknotesSerializers
    queryset = model.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return self.list(request, *args, **kwargs)
        else:
            return Response({"message": "user must login"}, status=status.HTTP_400_BAD_REQUEST)
        # user=self.model.objects.get(user=self.request.user)



    def perform_create(self, serializer):
        user = self.request.user
        print(user)
        # serializer.user=self.request.user
        serializer.save(user=user)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class WorknotesDetailsView(generics.GenericAPIView,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    model=Worknotes
    serializer_class = WorknotesSerializers
    queryset = Worknotes.objects.all()
    lookup_field = "id"
    # authentication_classes = [BasicAuthentication,SessionAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def perform_update(self, serializer):
        user=self.request.user
        serializer.save(user=user)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)