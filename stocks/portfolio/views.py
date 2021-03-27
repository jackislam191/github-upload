from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quotes.models import Position
# Create your views here.
@login_required
def portfolio_overview(request):
    user_holding = Position.objects.filter(created_by = request.user)
    len_userholding = len(user_holding)
    user_holding_dict = list(Position.objects.filter(created_by = request.user).values())
    
    
    #print(user_portfolio['AAPL']['id']) --->1
    
        #---> 1,4,5,10
    context = {
        'portfolio': user_holding_dict

    }
    return render(request, 'portfolio/overview.html', context)