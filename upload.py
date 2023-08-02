#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#
import logging.config
import sys

from transformers import AutoTokenizer, AutoModelForSequenceClassification

from consts import MODEL_DIR, HF_MODEL_ID
from consts import HF_DATASET_ID
from utils import read_dataset

logging.config.fileConfig('logging.conf')
log = logging.getLogger('main')

model_args = {
    'repo_id': HF_MODEL_ID,
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
    log.info('Uploading model and tokenizer...')
    for mt in [AutoModelForSequenceClassification, AutoTokenizer]:
        mt.from_pretrained(MODEL_DIR).push_to_hub(**model_args)

    # upload the dataset
    log.info('Uploading dataset...')
    dataset = read_dataset()
    dataset.push_to_hub(**dataset_args)

    log.info('Done.')
