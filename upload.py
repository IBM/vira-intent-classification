#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#
import sys

from transformers import AutoTokenizer, AutoModelForSequenceClassification

from consts import MODEL_DIR, HF_MODEL_ID
from consts import HF_DATASET_ID
from utils import read_dataset

model_args = {
    'repo_path_or_name': f'{MODEL_DIR}_hf',
    'repo_url': HF_MODEL_ID,
}

dataset_args = {
    'repo_id': HF_DATASET_ID,
}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Syntax: {sys.argv[0]} <auth-token>")
        exit(1)

    # add the auth token to the args
    model_args.update({'use_auth_token': sys.argv[1]})
    dataset_args.update({'token': sys.argv[1]})

    # upload the model and the tokenizer
    for mt in [AutoModelForSequenceClassification, AutoTokenizer]:
        mt.from_pretrained(MODEL_DIR).push_to_hub(**model_args)

    # upload the dataset
    dataset = read_dataset()
    dataset.push_to_hub(**dataset_args)