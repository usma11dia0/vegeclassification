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
from PIL import Image


#ファインチューニング(全結合層を調整)
class Net(pl.LightningModule):

    def __init__(self):
        super().__init__()

        self.feature = resnet18(pretrained=True)
        self.fc = nn.Linear(1000, 3)


    def forward(self, x):
        h = self.feature(x)
        h = self.fc(h)
        return h


    def training_step(self, batch, batch_idx):
        x, t = batch
        y = self(x)
        loss = F.cross_entropy(y, t)
        self.log('train_loss', loss, on_step=False, on_epoch=True)
        self.log('train_acc', accuracy(y.softmax(dim=-1), t), on_step=False, on_epoch=True)
        return loss


    def validation_step(self, batch, batch_idx):
        x, t = batch
        y = self(x)
        loss = F.cross_entropy(y, t)
        self.log('val_loss', loss, on_step=False, on_epoch=True)
        self.log('val_acc', accuracy(y.softmax(dim=-1), t), on_step=False, on_epoch=True)
        return loss


    def test_step(self, batch, batch_idx):
        x, t = batch
        y = self(x)
        loss = F.cross_entropy(y, t)
        self.log('test_loss', loss, on_step=False, on_epoch=True)
        self.log('test_acc', accuracy(y.softmax(dim=-1), t), on_step=False, on_epoch=True)
        return loss


    def configure_optimizers(self):
        optimizer = torch.optim.SGD(self.parameters(), lr=0.01)
        return optimizer


#推論 前処理用
def classify(img_url):

    #推論前の前処理
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor()
    ])

    target_img = transform(Image.open(img_url))
    target_img = target_img.unsqueeze(0)

    #推論の実行
    #ネットワークの準備（推論モード)
    net = Net().cpu().eval()
    #重みの読込
    net.load_state_dict(torch.load("model/vegetable.pt",map_location=torch.device('cpu')))

    #予測値の計算
    result = net(target_img).float()

    #確率に変換
    result_proba = F.softmax(result, dim=1)

    #確率.ラベル取得
    y_proba = torch.max(result_proba).item()
    y = torch.argmax(result_proba).item()

    #結果表記調整
    y_proba = y_proba*100

    #推論結果をHTMLに渡す
    return y, y_proba
