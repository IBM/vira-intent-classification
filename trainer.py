#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#
import evaluate
import numpy as np
from datasets import load_dataset
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import AutoTokenizer, DataCollatorWithPadding

from consts import MODEL_DIR, HF_DATASET_ID, BASE_MODEL, N_EPOCHS, LEARNING_RATE
from utils import read_dataset


def run_trainer(dataset, n_labels):
    metric = evaluate.load("accuracy")
    model_name = BASE_MODEL
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=n_labels)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def compute_metrics(p):
        logits, labels = p
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

    def preprocess_function(examples):
        return tokenizer(examples["text"], truncation=True)

    tokenized_dataset = dataset.map(preprocess_function, batched=True)

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    training_args = TrainingArguments(
        output_dir=MODEL_DIR,
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=N_EPOCHS,
        load_best_model_at_end=True,
        save_total_limit=1,
        save_strategy='epoch',
        evaluation_strategy='epoch',
        metric_for_best_model='accuracy',
        seed=123
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model()
    return trainer.evaluate()


def main():
    use_local_dataset = True

    if use_local_dataset:
        # load the dataset from the file system
        dataset = read_dataset()
    else:
        # load the dataset from hugging face
        dataset = load_dataset(HF_DATASET_ID)

    # determine the number of labels
    n_labels = max(dataset['train']['label']) + 1

    # train and eval on the validation set
    eval_result = run_trainer(dataset, n_labels)
    print(f'Accuracy on the validation set: {eval_result["eval_accuracy"]}')


if __name__ == '__main__':
    main()
