from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from .forms import UserChangeForm

from news.models import Author

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http.response import HttpResponse #импортируем респонс для проверки текста

from django.utils import timezone
import pytz  #импортируем стандартный модуль для работы с часовыми поясами


class IndexView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account/signin.html'
    form_class = UserChangeForm
    success_url = '/'

    def get_object(self, **kwargs):
        # id = self.kwargs.get('pk')
        return User.objects.get(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['current_time'] = timezone.now(),
        context['timezones'] = pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        return context

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    if not Author.objects.filter(user=user).exists():
        Author.objects.create(name=user.username, user=user)
    return redirect('/')
