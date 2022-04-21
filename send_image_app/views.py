#from unittest import result
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from model.predict import classify
from .forms import ImageForm, LoginForm, SignUpForm
from .models import ModelFile, VegeInformation

@login_required
def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_name = request.FILES['image']
            img_url = 'media/documents/{}'.format(img_name)
            y, y_proba = classify(img_url)

            #推論結果を保存
            modelfile = ModelFile.objects.order_by('id').reverse()[0]
            modelfile.proba = y_proba
            modelfile.result = y
            modelfile.save()

            #結果出力用に修正
            vegedata = VegeInformation.objects.all().get(label=y)
            y_name = vegedata.name
            knowledge = vegedata.knowledge


        return render(request,'send_image_app/classify.html',
                        {'y_name':y_name,
                        'y_proba':round(y_proba,2),
                        'img_url':img_url,
                        'knowledge':knowledge
                        }
                     )
    else:
        form = ImageForm()
        return render(request, 'send_image_app/index.html', {'form':form})

class Login(LoginView):
    form_class = LoginForm
    template_name = 'send_image_app/login.html'

class Logout(LogoutView):
    template_name = 'send_image_app/base.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username =  form.cleaned_data.get('username')
            password =  form.cleaned_data.get('password1')
            new_user = authenticate(username=username,password=password)
            if new_user is not None:
                login(request,new_user)
            return redirect('index')
        else:
           form = SignUpForm()
           return render(request, 'send_image_app/signup.html', {'form':form}) 
    else:
        form = SignUpForm()
        return render(request, 'send_image_app/signup.html', {'form':form})
    
