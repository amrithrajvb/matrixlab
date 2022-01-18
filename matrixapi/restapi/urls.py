from django.urls import path
from restapi import views

urlpatterns=[
    path("member/accounts/signup", views.UserCreationView.as_view()),
    path("member/accounts/signin", views.SigninView.as_view()),
    path("member/worknotes/adding", views.WorknotesAddView.as_view()),
    path("member/worknotes/details/<int:id>", views.WorknotesDetailsView.as_view()),
]