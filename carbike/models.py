from django.db import models

import io, base64
from PIL import Image
import os, glob
import numpy as np
from torchvision import datasets, transforms
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import torchvision
import cloudpickle


class Photo(models.Model):
    image = models.ImageField(upload_to='photos')

    IMAGE_SIZE = 224 # モデルに入力する画像サイズ
    MODEL_FILE_PATH = './carbike/ml_models/model.ckpt' # モデルファイル
    classes = ["car", "motorbike"]
    num_classes = len(classes)

    # device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    device='cpu'

    # 引数から画像ファイルを参照して読み込む
    def predict(self):

        # モデルロード
        model = torchvision.models.resnet18(pretrained=False)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, 2) # 1000の出力数を2に変換
        model.load_state_dict(torch.load(self.MODEL_FILE_PATH, map_location='cpu'))

        img_data = self.image.read()
        img_bin = io.BytesIO(img_data)

        # 画像の変換
        image = Image.open(img_bin)
        image = image.convert("RGB")
        image = image.resize((self.IMAGE_SIZE, self.IMAGE_SIZE))
        data = np.asarray(image) / 255.0
        X = []
        X.append(data)
        X = np.array(X)

        # tensorに変換
        X = torch.from_numpy(X)
        X = X.to(device=self.device, dtype=torch.float)
        X = X.permute(0, 3, 1, 2)

        model.eval() 
        with torch.no_grad():
            outputs = model(X)
            _, predicted = torch.max(outputs.data, 1)

        return self.classes[predicted]

    def image_src(self):
        with self.image.open() as img:
            base64_img = base64.b64encode(img.read()).decode()

            return 'data:' + img.file.content_type + ';base64,' + base64_img


