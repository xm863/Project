from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, TemplateView, DetailView,
    CreateView, FormView,
)
from.models import Food, Categories, New, Theme
from httpx import get
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .mixins import NotLoginRequiredMixin
from .forms import UserCreateForm, UserLoginForm, CommentForm
from.models import Users, Comment
from django.contrib.auth import login, logout
BOT_TOKEN = "7973924292:AAFEkXC8ok-8D2MHnS61yOEG0yUFUEi4BMQ"

class IndexView(TemplateView):
    template_name = 'index.html'    

class MenuView(ListView):
    model = Food
    template_name = 'menu.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        food = Food.objects.all()
        categories = Categories.objects.all()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['food'] = food
        context['category'] = categories
        return context


class ContactView(TemplateView):
    template_name = 'contact.html'

def send_message (chat_id, message) :
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = get(url, params=params)

def contactview(request):
    if request.method == 'POST':
        data = request.POST
        full_name = data.get('contact-name')
        email = data.get('contact-email')
        phone = data.get('contact-phone')
        message = data.get('contact-message')
        text = f"""
Foydalanuvchi ismi: {full_name}
Foydalanuvchi email: {email}
Foydalanuvchi nomeri: {phone}
Foydalanuvchi habari: {message}
"""
        send_message(6009060328, text)
    return render(request, 'contact.html')

class AboutView(TemplateView):
    template_name = 'about.html'

class NewsView(ListView):
    model = New
    template_name = 'news.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        news = New.objects.all()
        theme = Theme.objects.all()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['news'] = news
        context['theme'] = theme
        return context

class NewsDetailView(DetailView):
    model = New
    template_name = 'news-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.get_object()
        context['theme'] = Theme.objects.all()
        context['comments'] = Comment.objects.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        news = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                comment.user = Users.objects.get(username="Anonymous")  
            comment.save()
            return redirect('news-detail', pk=news.pk)
        return self.get(request, *args, **kwargs)

    
class UserCreateView(NotLoginRequiredMixin, CreateView):
    model = Users
    form_class = UserCreateForm
    template_name = 'register.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['username']

        if Users.objects.filter(username=username).exists():
            form.add_error('username', 'Bu username ishlatilgan.')
            return self.form_invalid(form)
        
        response = super().form_valid(form)  
        return response 

class UserSigninView(FormView):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = '/'


    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = Users.objects.filter(username=username).first()
        if user and user.check_password(password):
            login(self.request, user)
            return redirect('/')
        return super().form_valid(form)


class UserLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')
    
