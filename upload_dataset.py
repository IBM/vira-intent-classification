#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#
import sys

from consts import HF_DATASET_ID
from utils import read_dataset

dataset_args = {
    'repo_id': HF_DATASET_ID,
}


def main():
    if len(sys.argv) != 2:
        print(f"Syntax: {sys.argv[0]} <auth-token>")
        exit(1)

    # add the auth token to the args
    dataset_args.update({'token': sys.argv[1]})

    # upload the dataset
    dataset = read_dataset()
    dataset.push_to_hub(**dataset_args)


if __name__ == '__main__':
    main()
