---
title: HW3 - Big vs Small Models

---

# HW3 - Big vs Small Models

This assignment explores the relationship between **model size**, **training dataset size**, and **classification accuracy** using ResNet models on the CIFAR-10 dataset.

---

## 📁 Files

| File Name                      | Model     | Dataset Size | Description |
|-------------------------------|-----------|---------------|-------------|
| `resnet18_data-1-16.ipynb`    | ResNet-18 | 1/16          | Train ResNet-18 on a small portion of the dataset to observe underfitting behavior. |
| `resnet18_data-50.ipynb`      | ResNet-18 | 50%           | Train ResNet-18 on half of the dataset to evaluate mid-scale performance. |
| `resnet18_data-100.ipynb`     | ResNet-18 | 100%          | Train ResNet-18 on the full dataset for best-case performance. |
| `resnet50_data-1-16.ipynb`    | ResNet-50 | 1/16          | Train ResNet-50 with limited data to compare performance vs smaller model. |
| `resnet50_data-50.ipynb`      | ResNet-50 | 50%           | Medium dataset size experiment with deeper model. |
| `resnet50_data-100.ipynb`     | ResNet-50 | 100%          | Full data, full model training to compare accuracy vs ResNet-18. |

---

## 📊 Training Curves

The following plots compare the training/validation accuracy and loss across models and dataset sizes.

### 🔹 Accuracy Curves

| Model     | 1/16 Dataset | 50% Dataset | 100% Dataset |
|-----------|--------------|-------------|--------------|
| ResNet-18 | ![acc18-1-16](images/resnet18_acc_1-16.png) | ![acc18-50](images/resnet18_acc_50.png) | ![acc18-100](images/resnet18_acc_100.png) |
| ResNet-50 | ![acc50-1-16](images/resnet50_acc_1-16.png) | ![acc50-50](images/resnet50_acc_50.png) | ![acc50-100](images/resnet50_acc_100.png) |

### 🔹 Loss Curves

| Model     | 1/16 Dataset | 50% Dataset | 100% Dataset |
|-----------|--------------|-------------|--------------|
| ResNet-18 | ![loss18-1-16](images/resnet18_loss_1-16.png) | ![loss18-50](images/resnet18_loss_50.png) | ![loss18-100](images/resnet18_loss_100.png) |
| ResNet-50 | ![loss50-1-16](images/resnet50_loss_1-16.png) | ![loss50-50](images/resnet50_loss_50.png) | ![loss50-100](images/resnet50_loss_100.png) |

---

## 📝 Observations

- **Smaller datasets** lead to lower accuracy and higher variance.
- **ResNet-50** shows better performance on large datasets, but may overfit with small ones.
- Model size alone doesn't guarantee better accuracy — sufficient data is crucial.

---

