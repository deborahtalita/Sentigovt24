from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Bacapres
from .forms import BacapresForm
from django.contrib import messages
from sentigovt2.decorators import role_required
from django.core.paginator import Paginator
from django.http import JsonResponse


@role_required(allowed_roles=['ADMIN', 'SUPERADMIN'])
def bacapres_list(request):
    bacapres = Bacapres.objects.all().order_by('id')
    # pagination
    paginator = Paginator(bacapres, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    data_items = []
    for item in page_obj:
        data_item = {
            'id': item.id,
            'name': item.name,
            'avatar': item.avatar.url,
        }
        data_items.append(data_item)
    print(data_items)

    context = {
        'total_pages':paginator.num_pages,
        'results': data_items,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context, safe=False)
    else:
        context['active_page'] = 'bacapres management'
        return render(request, 'bacapres/bacapresManagement.html', context)

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
    context['active_page'] = 'bacapres management'
    return render(request, 'bacapres/createBacapres.html', context)

@role_required(allowed_roles=['ADMIN', 'SUPERADMIN'])
def edit_bacapres(request, id):
    context = {}
    bacapres = get_object_or_404(Bacapres,id=id)
    form = BacapresForm(request.POST,request.FILES, instance=bacapres)
    if request.method == "POST":
        if form.is_valid():
            new_img = form.cleaned_data['avatar']
            if new_img:
                form.cleaned_data['avatar'] = Bacapres.objects.get(id=id).avatar
            form.save()
            
    context['form'] = form
    context['object'] = bacapres
    context['active_page'] = 'bacapres management'
    return render(request,'bacapres/editBacapres.html', context)

@role_required(allowed_roles=['ADMIN', 'SUPERADMIN'])
def delete_bacapres(request, id):
    context = {}
    try:
        bacapres = get_object_or_404(Bacapres, id=id)
        bacapres.delete()
        return JsonResponse({'message': 'Data deleted successfully'})
    except Bacapres.DoesNotExist:
        return JsonResponse({'message': 'Invalid request method'})