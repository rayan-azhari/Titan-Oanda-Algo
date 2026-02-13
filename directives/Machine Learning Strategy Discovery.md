# Directive: Machine Learning Strategy Discovery

## Goal

Train and validate a Machine Learning model to predict **price direction** (Classification) or **future returns** (Regression), utilising VectorBT Pro for efficient pipeline management.

## Inputs

- Raw Parquet data from `.tmp/data/raw`
- Feature definitions (e.g., RSI, SMA, Volatility, Time of Day)

## Execution Steps

### 1. Feature Engineering

- Run `execution/build_ml_features.py`.
- Create a **Feature Matrix** ($X$) and **Target Vector** ($y$).

> [!CAUTION]
> **Crucial:** Shift targets backwards by 1 period to prevent look-ahead bias.

### 2. Model Training (Walk-Forward)

- Run `execution/train_ml_model.py`.
- Use `vbt.Splitter` to create expanding or rolling windows *(simulating real-time learning)*.
- Train an `XGBClassifier` or `RandomForest` on the train set; predict on the test set.
- Ensure `random_state=42` is set for reproducibility.

### 3. Performance Evaluation

- Generate a **Confusion Matrix** and **Feature Importance** plot.
- Calculate the **Sharpe Ratio** of the predicted signals, not just the model accuracy.

### 4. Model Serialisation

- If Sharpe Ratio > **1.5** on the test set, save the trained model to `models/production_model_v1.joblib`.

## Outputs

- Trained Model File (`.joblib`) in `models/`
- HTML Report: Feature Importance & Equity Curve