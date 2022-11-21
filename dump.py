#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#
from datasets import load_dataset


dataset_path = 'ibm/vira-intents'
dataset = load_dataset(dataset_path)


# assume that we have already loaded the dataset called "dataset"
for split, data in dataset.items():
    data.to_csv(f"my-dataset-{split}.csv", index=None)
