from django.shortcuts import render
#from django.http import HttpResponse  確認用

def index(request):
    return render(request, '../templates/send_image_app/index.html')
