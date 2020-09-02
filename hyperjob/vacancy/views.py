from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView
from vacancy.models import Vacancy


class MenuView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'menu.html')


class VacanciesView(View):

    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()
        return render(request, 'vacancies.html', {'vacancies': vacancies})


class MySignUpView(CreateView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = 'login'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class NewVacancyView(View):

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            desc = request.POST.get('description')
            Vacancy.objects.create(author=request.user, description=desc)
            return redirect('/vacancies/')
        else:
            raise PermissionDenied


class HomeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')
