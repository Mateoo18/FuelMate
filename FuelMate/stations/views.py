from django.shortcuts import render
from .models import Fuel
def fuel_list(request):
    fuels = Fuel.objects.all()
    return render(request, 'fuel_list.html', {'fuels': fuels})
