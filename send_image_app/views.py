from django.shortcuts import render

from model.predict import Net
from .forms import ImageForm
from .models import ModelFile

#モデル学習用のimport ※pip install要
import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms, datasets
from torchvision.models import resnet18
import pytorch_lightning as pl
import torchmetrics
from torchmetrics.functional import accuracy

def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_name = request.FILES['image']
            img_url = 'media/documents/{}'.format(img_name)
        return render(request, 'send_image_app/classify.html', {'img_url':img_url})
    else:
        form = ImageForm()
        return render(request, 'send_image_app/index.html', {'form':form})


def classify(request):
#学習済みモデルの読込
#loaded_model = joblib.load('model/predict.py')
#loaded_param = joblib.load('model/vegetable.pt')

    #Uploadされたデータを取得
    #data = ModelFile.objects.order_by('id').reverse().values_list('images') 
    #dataset = datasets.ImageFolder('/content/drive/MyDrive/Colab Notebooks/長期AI人材コース/機械学習アプリ/vegetable_images/train', transform)

    #前処理とアノテーション
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor()
    ])

    #推論の実行
    #学習済み重みをモデルへ付与する
    # classify_model = Net(data)
    # y = classify_model.predict(data)
    # y_proba = classify_model.predict_proba(data)

    #推論結果をHTMLに渡す
    # return render(request,'send_image_app/classify.html',{'y':y, 'y_proba':y_proba})
