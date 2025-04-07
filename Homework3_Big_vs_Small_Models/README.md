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

### 🔹 From Scratch

#### 🔹 Accuracy Curves

| Model     | 1/16 Dataset | 50% Dataset | 100% Dataset |
|-----------|--------------|-------------|--------------|
| ResNet-18 | ![acc18-1-16](images/from-scratch/resnet18_acc_1-16.png) | ![acc18-50](images/from-scratch/resnet18_acc_50.png) | ![acc18-100](images/from-scratch/resnet18_acc_100.png) |
| ResNet-50 | ![acc50-1-16](images/from-scratch/resnet50_acc_1-16.png) | ![acc50-50](images/from-scratch/resnet50_acc_50.png) | ![acc50-100](images/from-scratch/resnet50_acc_100.png) |

#### 🔹 Loss Curves

| Model     | 1/16 Dataset | 50% Dataset | 100% Dataset |
|-----------|--------------|-------------|--------------|
| ResNet-18 | ![loss18-1-16](images/from-scratch/resnet18_loss_1-16.png) | ![loss18-50](images/from-scratch/resnet18_loss_50.png) | ![loss18-100](images/from-scratch/resnet18_loss_100.png) |
| ResNet-50 | ![loss50-1-16](images/from-scratch/resnet50_loss_1-16.png) | ![loss50-50](images/from-scratch/resnet50_loss_50.png) | ![loss50-100](images/from-scratch/resnet50_loss_100.png) |


### 🔹 From Pretrained Weight

#### 🔹 Accuracy Curves

| Model     | 1/16 Dataset | 50% Dataset | 100% Dataset |
|-----------|--------------|-------------|--------------|
| ResNet-18 | ![acc18-1-16](images/finetune/resnet18_acc_1-16.png) | ![acc18-50](images/finetune/resnet18_acc_50.png) | ![acc18-100](images/finetune/resnet18_acc_100.png) |
| ResNet-50 | ![acc50-1-16](images/finetune/resnet50_acc_1-16.png) | ![acc50-50](images/finetune/resnet50_acc_50.png) | ![acc50-100](images/finetune/resnet50_acc_100.png) |

#### 🔹 Loss Curves

| Model     | 1/16 Dataset | 50% Dataset | 100% Dataset |
|-----------|--------------|-------------|--------------|
| ResNet-18 | ![loss18-1-16](images/finetune/resnet18_loss_1-16.png) | ![loss18-50](images/finetune/resnet18_loss_50.png) | ![loss18-100](images/finetune/resnet18_loss_100.png) |
| ResNet-50 | ![loss50-1-16](images/finetune/resnet50_loss_1-16.png) | ![loss50-50](images/finetune/resnet50_loss_50.png) | ![loss50-100](images/finetune/resnet50_loss_100.png) |

---

## 📝 Observations

### 🔹 Model Accuracy Summary

| Model                              | Dataset Size | Pretrained | Best Accuracy |
|-----------------------------------|--------------|------------|----------------|
| ResNet-18                         | 100%         | ❌         | 85.13%         |
| ResNet-50                         | 100%         | ❌         | 84.64%         |
| ResNet-18                         | 100%         | ✅         | 87.03%         |
| ResNet-50                         | 100%         | ✅         | 88.47%         |
| **ResNeXt50_32x4d**               | 100%         | ✅         | **89.31%**     |

By using a **pretrained ResNeXt50_32x4d** model (`weights="IMAGENET1K_V2"`), the best test accuracy of **89.31%** was achieved within only **20 epochs**.

---

### 🔹 Small Model Training Scenario (ResNet-18)

- Trained on 1/16, 50%, and 100% of the CIFAR-10 dataset.
- Accuracy increased proportionally with the dataset size, indicating that **small models benefit from larger datasets**.
- ResNet-18 is generally more stable with smaller data and trains faster, making it a good baseline model.

---

### 🔹 Large Model Training Scenario (ResNet-50)

- Also trained on 1/16, 50%, and 100% dataset splits.
- Larger models showed **greater gains on larger datasets** due to higher capacity, but may struggle with convergence on limited data.
- Some performance discrepancies were observed, likely due to **insufficient training epochs**. Deep models may require more time to converge and learn meaningful patterns.
- Increasing the number of epochs or using better training strategies may improve performance.

---

### 🔹 Effect of Pretrained Weights

- **Using ImageNet-pretrained weights** significantly improved accuracy across all dataset sizes.
- Pretrained models converged faster and achieved **higher accuracy**, especially on smaller datasets due to better feature initialization.
- However, they may also be more prone to **overfitting**, particularly when the dataset is small.

To mitigate overfitting:
- Apply **regularization techniques** (e.g., dropout).
- Use **early stopping** and learning rate schedules.
- Monitor validation performance closely during training.

---

### 🔹 Final Remarks

- **Pretrained models**, particularly ResNeXt50, offer the **best performance**, but need careful training management.
- **Dataset size** plays a critical role in performance: more data consistently leads to better generalization.
- Balancing model complexity, dataset size, and training strategy is key to achieving optimal performance in deep learning tasks.


