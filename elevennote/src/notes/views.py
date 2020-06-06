from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)

from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Note

from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
from .forms import NoteForm
from .mixins import NoteMixin


class NoteList(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'notes/index.html'
    context_object_name = 'latest_note_list'

    def dispatch(self, *args, **kwargs):
        return super(NoteList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if "filter_title" in self.request.GET.keys():
            return Note.objects.filter(title__contains=self.request.GET['filter_title']).order_by('-pub_date')
        elif "filter_tag" in self.request.GET.keys():
            tags = self.request.GET['filter_tag']
            while tags[0] == ' ':
                tags = tags[1:]
            return Note.objects.filter(tags__contains=tags).order_by('-pub_date')
        else:
            return Note.objects.filter(access__contains=self.request.user).order_by('-pub_date')


class NoteDetail(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/detail.html'
    context_object_name = 'note'

    def dispatch(self, *args, **kwargs):
        return super(NoteDetail, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Note.objects.filter(access__contains=self.request.user)


class NoteCreate(LoginRequiredMixin, NoteMixin, CreateView):
    form_class = NoteForm
    template_name = 'notes/form.html'
    success_url = reverse_lazy('notes:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.pub_date = timezone.now()
        if str(self.request.user) not in form.instance.access:
            form.instance.access += ' '
            form.instance.access += str(self.request.user)
        return super(NoteCreate, self).form_valid(form)


class NoteUpdate(LoginRequiredMixin, NoteMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/form.html'

    def get_queryset(self):
        return Note.objects.filter(access__contains=self.request.user)

    def get_success_url(self):
        return reverse('notes:update', kwargs={
            'pk': self.object.pk
        })

    def form_valid(self, form):
        if str(self.request.user) not in form.instance.access:
            form.instance.access += ' '
            form.instance.access += str(self.request.user)
        return super(NoteUpdate, self).form_valid(form)


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('notes:create')

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
