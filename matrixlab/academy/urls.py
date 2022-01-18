from django.urls import path
from academy import views

urlpatterns=[
    path("wornotes/accounts/signup",views.UserRegistrationView.as_view(),name="signup"),
    path("worknotes/accounts/signin",views.SigninView.as_view(),name="signin"),
    path("worknotes/accounts/signin/admin", views.UserDeatails.as_view(), name="adminhome"),
path("worknotes/accounts/signin/admin/verify/<int:id>", views.ApprovedUser.as_view(), name="approved"),
path("worknotes/admin/approved/users/list", views.ApprovedUsers.as_view(), name="approvedusers"),
    path("worknotes/member/home",views.MemberHome.as_view(),name="memberhome"),
    path("worknotes/signout", views.SignOutView.as_view(), name="Signout"),
    path("worknotes/add/notes",views.AddingWorknotes.as_view(),name="worknotes"),
    path("worknotes/view/notes",views.DetailWorknotes.as_view(),name="viewworknotes"),
    path("worknotes/change/notes/<int:id>",views.WorknotesEditView.as_view(),name="editworknotes"),
    path("worknotes/remove/notes/<int:id>",views.RemoveNotes.as_view(),name="removeworknotes"),
    ]