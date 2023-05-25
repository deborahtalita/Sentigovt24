from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Bacapres
from .forms import BacapresForm
from django.contrib import messages
from sentigovt2.decorators import role_required


@role_required(allowed_roles=['ADMIN', 'SUPERADMIN'])
def bacapres_list(request):
    bacapres = Bacapres.objects.all().order_by('id')
    data = {}
    data['obj_list'] = bacapres
    return render(request, 'bacapresManagement.html', data)

@role_required(allowed_roles=['ADMIN', 'SUPERADMIN'])
def create_bacapres(request):
    context = {}
    form = BacapresForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, ('Bacapres was succesfully added!'))
            return redirect(reverse_lazy('bacapres:bacapres_list'))
        else:
            messages.error(request, 'Error saving form')
            print(form.errors.as_data())
    context['form'] = form
    return render(request, 'createBacapres.html', context)

@role_required(allowed_roles=['ADMIN', 'SUPERADMIN'])
def edit_bacapres(request, id):
    context = {}
    bacapres = get_object_or_404(Bacapres,id=id)
    form = BacapresForm(request.POST,request.FILES, instance=bacapres)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('bacapres:bacapres_list'))
    context['form'] = form
    context['object'] = bacapres
    return render(request,'editBacapres.html', context)

@role_required(allowed_roles=['ADMIN', 'SUPERADMIN'])
def delete_bacapres(request, id):
    context = {}
    try:
        bacapres = get_object_or_404(Bacapres, id=id)
        bacapres.delete()
        return redirect(reverse_lazy('bacapres:bacapres_list'))
    except Bacapres.DoesNotExist:
        print("Object not found")
        return redirect(reverse_lazy('bacapres:bacapres_list'))