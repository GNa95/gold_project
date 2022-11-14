from django.shortcuts import render

# Create your views here.


def comm(request):
  return render(request, 'community/comm.html', {})