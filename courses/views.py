from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Note
from .forms import CourseForm, NoteForm
from django.db.models import Q


@login_required
def course_list_view(request):
    courses = Course.objects.filter(owner=request.user)
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required
def course_create_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()
            messages.success(request, 'Course created.')
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Create Course'})


@login_required
def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk, owner=request.user)
    notes = course.notes.all()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'notes': notes,
    })

@login_required
def course_edit_view(request, pk):
    course = get_object_or_404(Course, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated.')
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit Course'})


@login_required
def course_delete_view(request, pk):
    course = get_object_or_404(Course, pk=pk, owner=request.user)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted.')
        return redirect('courses:course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

@login_required
def note_create_view(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, owner=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.course = course
            note.save()
            messages.success(request, 'Note created.')
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = NoteForm()
    return render(request, 'courses/note_form.html', {'form': form, 'course': course})


@login_required
def note_edit_view(request, pk):
    note = get_object_or_404(Note, pk=pk, course__owner=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated.')
            return redirect('courses:course_detail', pk=note.course.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'courses/note_form.html', {'form': form, 'course': note.course})


@login_required
def note_delete_view(request, pk):
    note = get_object_or_404(Note, pk=pk, course__owner=request.user)
    course_pk = note.course.pk
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted.')
        return redirect('courses:course_detail', pk=course_pk)
    return render(request, 'courses/note_confirm_delete.html', {'note': note})


@login_required
def search_view(request):
    query = request.GET.get('q', '')
    notes = []
    
    if query:

        notes = Note.objects.filter(
            course__owner=request.user
        ).filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(course__title__icontains=query)
        ).distinct()  # حذف نتایج تکراری
    
    return render(request, 'courses/search_results.html', {
        'query': query,
        'notes': notes,
    })

