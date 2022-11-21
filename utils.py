#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#
import os

import pandas as pd
from datasets import Dataset, DatasetDict

from consts import DATASET_DIR


def read_dataset():
    train_file = os.path.join(DATASET_DIR, 'train.csv')
    validation_file = os.path.join(DATASET_DIR, 'validation.csv')

    def read_file(file):
        df = pd.read_csv(file)
        df = df[['sentence', 'label_idx']]
        df = df.rename(columns={'sentence': 'text', 'label_idx': 'label'})
        return Dataset.from_pandas(df)

    dataset = DatasetDict()
    dataset['train'] = read_file(train_file)
    dataset['validation'] = read_file(validation_file)

    return dataset
