from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import PerformanceReview
from .forms import PerformanceReviewForm
from employees.models import Employee


@login_required
def review_list(request):
    if request.user.is_hr():
        reviews = PerformanceReview.objects.select_related(
            'employee__user', 'reviewer'
        ).all()
    else:
        try:
            emp = request.user.employee
            reviews = PerformanceReview.objects.filter(employee=emp)
        except Employee.DoesNotExist:
            reviews = PerformanceReview.objects.none()

    return render(request, 'performance/list.html', {'reviews': reviews})


@login_required
def review_detail(request, pk):
    review = get_object_or_404(PerformanceReview, pk=pk)

    if not request.user.is_hr() and review.employee.user != request.user:
        messages.error(request, 'You can only view your own reviews.')
        return redirect('review_list')

    return render(request, 'performance/detail.html', {'review': review})


@login_required
def review_create(request):
    if not request.user.is_hr():
        messages.error(request, 'Access denied. Only HR/Admin can create reviews.')
        return redirect('review_list')

    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Performance review created successfully.')
            return redirect('review_detail', pk=review.pk)
    else:
        form = PerformanceReviewForm()

    return render(request, 'performance/form.html', {
        'form': form,
        'title': 'Add Performance Review',
    })


@login_required
def review_edit(request, pk):
    if not request.user.is_hr():
        messages.error(request, 'Access denied.')
        return redirect('review_list')

    review = get_object_or_404(PerformanceReview, pk=pk)

    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated.')
            return redirect('review_detail', pk=pk)
    else:
        form = PerformanceReviewForm(instance=review)

    return render(request, 'performance/form.html', {
        'form': form,
        'title': f'Edit Review: {review.employee.employee_code}',
    })


@login_required
def review_delete(request, pk):
    if not request.user.is_admin():
        messages.error(request, 'Only admin can delete reviews.')
        return redirect('review_list')

    review = get_object_or_404(PerformanceReview, pk=pk)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted.')
        return redirect('review_list')

    return render(request, 'performance/confirm_delete.html', {'review': review})