#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#

import logging.config
import os

import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

from consts import HF_MODEL_ID

logging.config.fileConfig('logging.conf')
log = logging.getLogger('services.dialog')

log.info('Initiating service')
app = FastAPI(openapi_url=None)

tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_ID)
model = AutoModelForSequenceClassification.from_pretrained(HF_MODEL_ID)
pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)
df = pd.read_csv(os.path.join('intent_dataset', 'intents.csv'))
model_trained_intents = df['intent'].apply(str.strip).to_list()

log.info('Service is ready')


def get_model_predictions(candidates):
    results = pipeline(candidates)
    intent_scores = np.array([[label['score'] for label in result] for result in results])
    intent_ids = np.argmax(intent_scores, axis=1)
    intent_scores = np.max(intent_scores, axis=1)
    model_intents = [model_trained_intents[intent_id] for intent_id in intent_ids]
    return model_intents, intent_scores.tolist()


@app.get("/")
def read_root():
    return "VIRA Intent Classification"


@app.get("/health")
def read_root():
    return "OK"


@app.get("/classify")
def read_root(text: str):
    return get_model_predictions([text])


if __name__ == '__main__':
    # intents, scores = get_model_predictions(['i love it', 'i hate it'])
    # print(intents, scores)
    uvicorn.run(app, host="0.0.0.0", port=8040)
