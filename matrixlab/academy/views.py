from academy import forms
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
# Create your views here.
from django.views.generic import CreateView,ListView,TemplateView,DetailView,UpdateView,DeleteView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from academy.models import MyUser, Worknotes
from academy.decorators import Sign_required
from django.utils.decorators import method_decorator


class UserRegistrationView(CreateView):
    model = MyUser
    form_class = forms.UserRegistrationForm
    template_name = 'academy/signup.html'
    success_url = reverse_lazy("signin")


class SigninView(TemplateView):
    template_name = 'academy/signin.html'
    form_class=forms.SigninForm

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["form"]=self.form_class()
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            print(email,password)
            if user:
                login(request, user)
                print(user)
                if request.user.role=="admin":
                    return redirect("adminhome")
                else:
                    if not request.user.is_admin:
                        messages.error(request, "Please wait for admin verification")
                        return redirect('signin')
                    else:
                        return redirect('memberhome')
            else:
                messages.error(request, "please enter correct username/password")
                return redirect('signin')

class SignOutView(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("signin")
@method_decorator(Sign_required,name='dispatch')
class MemberHome(TemplateView):
    template_name = 'academy/memberhome.html'

@method_decorator(Sign_required,name='dispatch')
class AddingWorknotes(CreateView):
    model = Worknotes
    form_class = forms.Notes
    template_name = 'academy/adding_worknotes.html'
    user=MyUser.objects.all()



    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST,files=request.FILES)
        # print(form)
        user = MyUser.objects.get(email=self.request.user)
        id=user.id
        print(id,"dfgdfgdf")
        print(request.user)
        if form.is_valid():
            notes=form.save(commit=False)
            notes.user=request.user
            print(notes.user)
            notes.save()
            return redirect("memberhome")
        else:
            return redirect("worknotes")

@method_decorator(Sign_required,name='dispatch')
class DetailWorknotes(TemplateView):
    model = Worknotes
    form_class = forms.Notes
    template_name = 'academy/view_worknotes.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        notes = self.model.objects.filter(user=self.request.user)
        return render(request, self.template_name, {"form": form, "notes": notes})

@method_decorator(Sign_required,name='dispatch')
class WorknotesEditView(UpdateView):
    model = Worknotes
    form_class = forms.Notes
    template_name = "academy/edit_worknotes.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy('viewworknotes')

@method_decorator(Sign_required,name='dispatch')
class RemoveNotes(DeleteView):
    model = Worknotes
    template_name = "academy/removenotes.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("viewworknotes")

@method_decorator(Sign_required,name='dispatch')
class UserDeatails(TemplateView):
    model = MyUser
    form_class = forms.UserRegistrationForm
    template_name = 'academy/adminhome.html'
    pk_url_kwarg = "id"


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user = self.model.objects.filter(is_admin=False)
        print(user,"users list")
        return render(request, self.template_name, {"form": form, "users": user})

@method_decorator(Sign_required,name='dispatch')
class ApprovedUser(TemplateView):
    model = MyUser
    form_class = forms.UserRegistrationForm
    template_name = 'academy/adminhome.html'
    pk_url_kwarg = "id"


    def get(self, request, *args, **kwargs):
        user=self.model.objects.get(id=kwargs["id"])
        user.is_admin=True
        user.save()
        return redirect("adminhome")

@method_decorator(Sign_required,name='dispatch')
class ApprovedUsers(TemplateView):
    model = MyUser
    form_class = forms.UserRegistrationForm
    template_name = 'academy/approvedusers.html'


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user = self.model.objects.filter(is_admin=True,role="member")
        print(user,"users list")
        return render(request, self.template_name, {"form": form, "users": user})

