from django.shortcuts import render

# <!---
#comp 3450 <Ashima,ripan>-->
def home(request):
    return render(request,"home.html",{})

def post(request):
    return render(request,"posts.html",{})

def detail(request):
    return render(request,"detail.html",{})

def lobby(request):
    return render(request, 'lobby.html',{})