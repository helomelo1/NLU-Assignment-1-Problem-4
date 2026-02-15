# Sports vs Politics Text Classification

This project implements a simple machine learning system to classify news articles into **Sports** or **Politics** categories.

The goal of this assignment was to compare different machine learning techniques and understand how they perform on text data.

---

## Dataset

The dataset used is the **BBC News Dataset**.

Only two categories were selected:

- Sports
- Politics

After filtering, the dataset contained:

- Sports: 346 articles  
- Politics: 274 articles  
- Total: 620 articles  

---

## Feature Representation

Text data was converted into numerical form using **TF-IDF vectorization** with unigram and bigram features.

This helps capture important words and short phrases.

---

## Models Used

Three machine learning models were compared:

1. Multinomial Naive Bayes  
2. Logistic Regression  
3. Support Vector Machine (SVM)  

---

## Experimental Setup

The dataset was split into training and testing sets using four different test sizes:

- 20% test split
- 40% test split
- 60% test split
- 80% test split

This was done to observe how model performance changes with different training data sizes.

---

## Results

All models performed very well because sports and politics articles contain very different vocabulary.

SVM and Naive Bayes consistently achieved the highest accuracy.

Accuracy decreased slightly when training data became smaller.

---
