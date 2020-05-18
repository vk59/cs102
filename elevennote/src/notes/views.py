from django.shortcuts import get_object_or_404, render

from .models import Note

from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    latest_note_list = Note.objects.filter(owner=request.user).order_by('-pub_date')[:5]
    context = {
        'latest_note_list': latest_note_list,
    }
    return render(request, 'notes/index.html', context)


@login_required
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id, owner=request.user)
    return render(request, 'notes/detail.html', {'note': note})
