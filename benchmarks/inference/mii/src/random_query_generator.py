# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team

import numpy as np
import torch
import random


class RandomQueryGenerator:
    def __init__(self, input_text, tokenizer, seed, use_openai_payload=False):
        self.input_text = input_text
        self.tokenizer = tokenizer
        self.use_openai_payload = use_openai_payload

        torch.manual_seed(seed)
        random.seed(seed)
        np.random.seed(seed)

    def get_random_request_text(self, length, variance, max_length, batch):
        request_text = []
        if self.use_openai_payload is True:
            tokenized_input = self.tokenizer.encode(self.input_text)
            text_ids = tokenized_input
        else:
            tokenized_input = self.tokenizer.batch_encode_plus(
                [self.input_text], return_tensors="pt", padding=False
            )
            # TODO: consider different input text and initialize at different intervals
            # currently most of the input prompt is similar
            text_ids = tokenized_input["input_ids"][0]

        offset = list(range(512))
        random.shuffle(offset)

        for i in range(batch):
            # Set max_new_tokens following normal distribution with mean=max_new_tokens and std=0.3*max_new_tokens
            req_prompt_length = min(int(np.random.normal(length, variance)), max_length)

            text = self.tokenizer.decode(text_ids[i : req_prompt_length + i])
            request_text.append(text)
        return request_text
