from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from base.models import Tasks


# Create your views here.

class UserLogin(LoginView):
    template_name = 'forms.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'login'
        context['btntxt'] = 'login'
        return context


class UserRegister(FormView):
    template_name = 'forms.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        context['btntxt'] = 'Register'
        return context

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegister, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(UserRegister, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks.html'

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['object_list'] = context['object_list'].filter(user=self.request.user)
        context['comp_count'] = context['object_list'].filter(complete=False).count()

        seacher = self.request.GET.get('seacher') or ''
        if seacher:
            context['object_list'] = context['object_list'].filter(title__icontains=seacher)

        context['seacher'] = seacher
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = 'task_details.html'
    context_object_name = 'objects'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Tasks
    template_name = 'forms.html'
    fields = ['title', 'descriptions', 'complete']
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'create'
        context['btntxt'] = 'create'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Tasks
    fields = ['title', 'descriptions', 'complete']
    template_name = 'forms.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'update'
        context['btntxt'] = 'update'
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Tasks
    template_name = 'forms.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'delete'
        context['btntxt'] = 'delete'
        return context
