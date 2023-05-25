from django.shortcuts import render
from django.http import HttpResponse
from sentiment.models import Bacapres
import uuid
from accounts.models import Session


def home(request):
    
    return render(request, 'home.html')

def dashboard(request):
    context = {}

    if 'selected_options' in request.session:
        del request.session['selected_options']
    
    if 'selected_start_date' in request.session:
        del request.session['selected_start_date']
    
    if 'selected_end_date' in request.session:
        del request.session['selected_end_date']
    
    if 'history_id' in request.session:
        del request.session['history_id']

    # get bacapres
    bacapres = Bacapres.objects.all().order_by('id')
    context['bacapres'] = bacapres

    active_item = bacapres.first()
    if active_item: context['active_item'] = active_item.id
    
    print(active_item.id)

    context['title'] = 'Dashboard'
    context['active_page'] = 'dashboard'

    rendered_html = render(request, 'dashboard.html', context)

    # set session for guest
    session_id = request.COOKIES.get('session_id')
    if session_id:
        response = HttpResponse(rendered_html)
    else:
        response = HttpResponse(rendered_html)
        
        unique_id = str(uuid.uuid4())
        session_age = 3600 * 24 * 90 # 3 months
        response.set_cookie('session_id', unique_id, max_age=session_age)
        session = Session.objects.create(id=unique_id)
        session.save()

    return response