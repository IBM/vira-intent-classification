#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#
import os

DATASET_DIR = os.path.join('.', 'intent_dataset')
MODEL_DIR = os.path.join('.', 'intent_model')

# BASE_MODEL = 'roberta-large'
# N_EPOCHS = 15
BASE_MODEL = 'roberta-base'
N_EPOCHS = 1
LEARNING_RATE = 5e-6

HF_DATASET_ID = "ibm/vira-intents-live"
HF_MODEL_ID = f'ibm/{BASE_MODEL}-vira-intents-live'
