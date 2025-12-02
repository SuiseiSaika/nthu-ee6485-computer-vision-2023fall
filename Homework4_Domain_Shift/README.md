# **Homework #4 — Handling Domain Shift**

This assignment investigates how different data-splitting, data-selection, and semi-supervised learning strategies influence YOLOv7 performance under domain shift. Using the CityCam dataset—which consists of multi-camera surveillance images with inconsistent visual distributions—we design Q1, Q2, and Q3 experiments to systematically evaluate the model’s robustness. Evaluation metrics are **mAP@0.5** and **mAP@0.5:0.95** across all experiments.

---

## **Q1 — Baseline Training and Camera-Wise Performance**

The first task aims to analyze the effect of basic train/validation splitting on model generalization.

### **Implementation**

We implemented `split_train_val_path()` which:

* Randomly shuffles all image paths using `random.shuffle()`
* Splits training/validation sets using `train_val_ratio`
* Generates the YAML configuration file for YOLOv7 training

### **Observations**

Training a YOLO model on the Q1 dataset produces camera-specific performance variations. Some cameras achieve strong detection accuracy, while others suffer notable drops due to differences in scene geometry, lighting, or object density.

This result indicates that **Q1 alone introduces camera bias and insufficient diversity**, motivating further exploration of alternative sampling strategies.

---

## **Q2 — Comparison of Data Selection Strategies**

Q2 evaluates how different image sampling approaches impact performance. Six strategies were designed:

### **2-1. Random Shuffle**

Randomly select images without considering camera identity.

* Pros: avoids ordering bias
* Cons: may cause unbalanced camera distribution

### **2-2. Averagely Random Shuffle**

Ensures equal representation from each camera.

* Pros: reduces camera imbalance
* Cons: random selection still introduces sampling variance

### **2-3. Select by Most Objects**

Select images containing the highest number of objects.

* Pros: encourages dense supervision
* Cons: may overrepresent naturally crowded cameras

### **2-3\*. Averagely Select by Most Objects**

Balances object-rich images across all cameras.

### **2-4. Select by Most Classes**

Prefer images containing the largest set of distinct object categories.

* Pros: encourages training diversity
* Cons: class-dominant cameras may take over

### **2-4\*. Averagely Select by Most Classes**

Ensures class-diverse images per camera.

### **Results Summary**

Across all six strategies:

* All methods outperform the Q1 baseline.
* **2-2**, **2-3**, and **2-3*** consistently show the best performance.
* Balanced sampling + information-rich selection leads to higher **mAP@0.5** and **mAP@0.5:0.95**.
* Camera bias decreases when ensuring per-camera fairness.

**Conclusion:** Q2 demonstrates that training data composition—both in balance and informational richness—is crucial for generalizable detection performance.

---

## **Q3 — Domain Adaptation Strategies**

Q3 focuses on methods that reduce domain shift between Q2/Q3 datasets.

### **3-1. Pseudo Labeling**

* Use the best Q2 model (2-2) to generate pseudo labels on Q3.
* Apply confidence filtering to control label quality.
* Significantly increases the amount of training data.

### **3-2. Incorporate 200 Labeled Q2 Samples**

* Add 200 labeled images from Q2 (constraint requirement).
* Initialize training using Q2-2 weights.
* Provides additional diversity, improving generalization.

### **3-3. Freeze Backbone**

* Apply `--freeze 50` to YOLOv7.
* Keeps early feature representations stable.
* Prevents catastrophic forgetting while adapting to Q3.

### **3-4. Positive Class Weights**

* Adjust positive weights from 1.0 → 5.0.
* Mitigates class imbalance during fine-tuning.

### **3-5. Focal Loss**

* Increase focal loss from 0.0 → 1.5.
* Emphasizes hard-to-classify examples.
* Slight improvement in mAP@0.5:0.95.

### **Results Summary**

Across the five strategies:

* **3-2** and **3-3** are the strongest overall performers.
* Pseudo labels (3-1) help but depend heavily on threshold quality.
* Weighting and focal loss (3-4, 3-5) provide consistent but smaller gains.

**Conclusion:** Semi-supervised labeling, backbone freezing, and diverse initialization all contribute to more stable domain adaptation. The combination of data diversity and targeted fine-tuning yields the most robust performance.

---

## **Final Conclusion**

Across Q1–Q3, several important findings emerge:

### **1. Camera-wise data imbalance strongly influences performance**

Q1 reveals that uneven training distribution results in camera bias, affecting generalization.

### **2. Balanced sampling + information-rich images give the best results**

Q2 strategies (especially **2-2**, **2-3**, **2-3*** ) show that selecting images with attention to both fairness and content quality boosts performance.

### **3. Domain adaptation is crucial for cross-dataset robustness**

Q3 demonstrates that pseudo labeling, freezing backbones, reweighting classes, and focal loss all help bridge the domain gap.

### **4. Data composition is more important than model architecture**

Across all experiments, the data selection and domain adaptation strategies have a larger impact on performance than model changes alone.

---


Environment
Python 3.8+

PyTorch 1.13+

YOLOv7 repository (https://github.com/WongKinYiu/yolov7)

NVIDIA GPU (tested on RTX 3090)
