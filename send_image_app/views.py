from unittest import result
from django.shortcuts import render

from model.predict import classify
from .forms import ImageForm
from .models import ModelFile

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

        return render(request,
                     'send_image_app/classify.html',
                     {'y':y, 'y_proba':round(y_proba,2),'img_url':img_url}
                     )
    else:
        form = ImageForm()
        return render(request, 'send_image_app/index.html', {'form':form})