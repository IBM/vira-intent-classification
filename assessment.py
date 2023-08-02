import os.path

from service import get_model_predictions, model_trained_intents
from consts import DATASET_DIR
import pandas as pd
import numpy as np
from sklearn.preprocessing import label_binarize
from sklearn.metrics import precision_recall_curve
import logging


def tune_threshold():
    df = pd.read_csv(os.path.join(DATASET_DIR, "validation.csv"))
    candidates = df['sentence'].tolist()
    num_classes = len(model_trained_intents)

    prediction_classes, prediction_scores = get_model_predictions(candidates)
    y_labels = label_binarize(df['label_idx'].tolist(), classes=[i for i in range(num_classes)])
    y_scores = np.array([[scores[0] if i == model_trained_intents.index(pred_classes[0]) else 0
                          for i in range(num_classes)]
                         for scores, pred_classes in zip(prediction_scores, prediction_classes)])

    precision, recall, thresholds = precision_recall_curve(
            y_labels.ravel(), y_scores.ravel()
        )
    thresholds = np.append(thresholds, 1)
    f1 = [2*p*r/(r+p) for p, r in zip(precision, recall)]
    best_index = np.argmax(f1)

    logging.info(f'Best threshold: {thresholds[best_index]}, best f1: {f1[best_index]}')

    return thresholds[best_index]


if __name__ == "__main__":
    tune_threshold()