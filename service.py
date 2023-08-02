#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#

import logging.config
import os
from typing import List

import pandas as pd
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

from consts import HF_MODEL_ID

logging.config.fileConfig('logging.conf')
log = logging.getLogger('main')

log.info('Initiating service')
app = FastAPI(openapi_url=None)

tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_ID)
model = AutoModelForSequenceClassification.from_pretrained(HF_MODEL_ID)
pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=None)
df = pd.read_csv(os.path.join('intent_dataset', 'intents.csv'))
model_trained_intents = df['intent'].apply(str.strip).to_list()

log.info('Service is ready')


def get_model_predictions(candidates):
    log.info('Getting model predictions')
    results = pipeline(candidates)
    intents = [[model_trained_intents[int(label['label'][6:])] for label in result]
               for result in results]
    scores = [[label['score'] for label in result]
              for result in results]
    return intents, scores


@app.get("/")
def read_root():
    return "VIRA Intent Classification"


@app.get("/health")
def health():
    return "OK"


class RequestModel(BaseModel):
    text: str


class ResponseModel(BaseModel):
    intents: List[str]
    scores: List[float]


@app.post("/classify", response_model=ResponseModel)
def classify(request: RequestModel):
    intents, scores = get_model_predictions([request.text])
    return ResponseModel(intents=intents[0], scores=scores[0])


def main():
    # intents, scores = classify("is the vaccine safe?")
    # print(intents, scores)
    uvicorn.run(app, host="0.0.0.0", port=8110)


if __name__ == '__main__':
    main()
