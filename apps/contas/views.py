from django.shortcuts import render

def timeout_view(request):
    return render(request, 'timeout.html')