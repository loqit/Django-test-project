from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
import logging

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView

from .forms import AuthUserForm, RegisterUserForm
from .models import Article, Comment
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy

from .token_generator import account_activation_token

logger = logging.getLogger('django')


def index(request):
    latest_news = Article.objects.order_by('-pub_date')[:5]
    return render(request, 'arcticles/list.html', {'latest_news': latest_news})


def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    l = article.comment_set.order_by('-id')[:10]
    return render(request, 'arcticles/detail.html', {'article': article, 'l': l})


@login_required
def leave_comment(request, article_id):
    a = get_object_or_404(Article, id=article_id)
    a.comment_set.create(author_name=request.user.username, comment_text=request.POST['text'], pub_date=timezone.now())
    return HttpResponseRedirect(reverse('main_page:detail', args=(a.id,)))


@login_required
def create_article(request):
    name = request.user.username
    Article.objects.create(article_title=request.POST.get('name'), article_text=request.POST.get('text'),
                           pub_date=timezone.now(), author_name=name)
    return HttpResponseRedirect(reverse('main_page:index'))


def home(request):
    return render(request, 'arcticles/home.html')


def delete_article(request, article_id):
    a = get_object_or_404(Article, id=article_id)
    a.delete()
    return HttpResponseRedirect(reverse('main_page:index'))


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    a = comment.article
    return HttpResponseRedirect(reverse('main_page:detail', args=(a.id,)))


class UserLoginView(LoginView):
    template_name = 'login_form.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('main_page:home')

    def get_success_url(self):
        logger.info('Successfully going to home page')
        return self.success_url


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class UserRegisterView(CreateView):
    model = User
    template_name = 'register_form.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')
    success_msg = "Аккаунт успешно создан!"

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        logger.info("User " + username + " is successfully register")

        return form_valid


def usersignup(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            email_subject = 'Активация аккаунта'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Мы отправили вам письмо, пожалуйста, подтвердите ваш e-mail для завершения регистрации!')
    else:
        form = RegisterUserForm()

    return render(request, 'register_form.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')