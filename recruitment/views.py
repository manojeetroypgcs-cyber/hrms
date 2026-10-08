from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import JobPosting, Candidate, Application
from .forms import JobPostingForm, CandidateForm, ApplicationForm


# ---------- JOB POSTINGS ----------

@login_required
def job_list(request):
    jobs = JobPosting.objects.select_related('department').all()
    return render(request, 'recruitment/job_list.html', {'jobs': jobs})


@login_required
def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    applications = job.applications.select_related('candidate').all()
    return render(request, 'recruitment/job_detail.html', {
        'job': job,
        'applications': applications,
    })


@login_required
def job_create(request):
    if not request.user.is_hr():
        messages.error(request, 'Access denied.')
        return redirect('job_list')

    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, 'Job posting created.')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostingForm()

    return render(request, 'recruitment/job_form.html', {
        'form': form,
        'title': 'Post a Job',
    })


@login_required
def job_edit(request, pk):
    if not request.user.is_hr():
        messages.error(request, 'Access denied.')
        return redirect('job_list')

    job = get_object_or_404(JobPosting, pk=pk)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job posting updated.')
            return redirect('job_detail', pk=pk)
    else:
        form = JobPostingForm(instance=job)

    return render(request, 'recruitment/job_form.html', {
        'form': form,
        'title': f'Edit Job: {job.title}',
    })


# ---------- CANDIDATES ----------

@login_required
def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, 'recruitment/candidate_list.html', {'candidates': candidates})


@login_required
def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    applications = candidate.applications.select_related('job').all()
    return render(request, 'recruitment/candidate_detail.html', {
        'candidate': candidate,
        'applications': applications,
    })


@login_required
def candidate_create(request):
    if not request.user.is_hr():
        messages.error(request, 'Access denied.')
        return redirect('candidate_list')

    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, 'Candidate added.')
            return redirect('candidate_detail', pk=candidate.pk)
    else:
        form = CandidateForm()

    return render(request, 'recruitment/candidate_form.html', {
        'form': form,
        'title': 'Add Candidate',
    })


@login_required
def candidate_edit(request, pk):
    if not request.user.is_hr():
        messages.error(request, 'Access denied.')
        return redirect('candidate_list')

    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate updated.')
            return redirect('candidate_detail', pk=pk)
    else:
        form = CandidateForm(instance=candidate)

    return render(request, 'recruitment/candidate_form.html', {
        'form': form,
        'title': f'Edit Candidate: {candidate.full_name}',
    })


# ---------- APPLICATIONS ----------

@login_required
def application_create(request):
    if not request.user.is_hr():
        messages.error(request, 'Access denied.')
        return redirect('job_list')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save()
            messages.success(request, 'Application created.')
            return redirect('job_detail', pk=app.job.pk)
    else:
        initial = {}
        job_id = request.GET.get('job')
        if job_id:
            initial['job'] = job_id
        form = ApplicationForm(initial=initial)

    return render(request, 'recruitment/application_form.html', {
        'form': form,
        'title': 'Link Candidate to Job',
    })