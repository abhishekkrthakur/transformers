#!/usr/bin/env python
# coding: utf-8

# This script creates a super tiny model that is useful inside tests, when we just want to test that
# the machinery works, without needing to the check the quality of the outcomes.
#
# This version creates a tiny model through reduction of a normal pre-trained model, but keeping the
# full vocab, merges file, and thus also resulting in a larger model due to a large vocab size.
# This gives ~3MB in total for all files.
#
# If you want a 50 times smaller than this see `fsmt-make-super-tiny-model.py`, which is slightly more complicated
#
#
# It will be used then as "stas/tiny-wmt19-en-de"

# Build
from transformers import FSMTConfig, FSMTForConditionalGeneration, FSMTTokenizer


mname = "facebook/wmt19-en-de"
tokenizer = FSMTTokenizer.from_pretrained(mname)
# get the correct vocab sizes, etc. from the master model
config = FSMTConfig.from_pretrained(mname)
config.update(
    dict(
        d_model=4,
        encoder_layers=1,
        decoder_layers=1,
        encoder_ffn_dim=4,
        decoder_ffn_dim=4,
        encoder_attention_heads=1,
        decoder_attention_heads=1,
    )
)

tiny_model = FSMTForConditionalGeneration(config)
print(f"num of params {tiny_model.num_parameters()}")

# Test
batch = tokenizer.prepare_seq2seq_batch(["Making tiny model"])
outputs = tiny_model(**batch, return_dict=True)

print("test output:", len(outputs.logits[0]))

# Save
mname_tiny = "tiny-wmt19-en-de"
tiny_model.half()  # makes it smaller
tiny_model.save_pretrained(mname_tiny)
tokenizer.save_pretrained(mname_tiny)

print(f"Generated {mname_tiny}")

# Upload
# transformers-cli upload tiny-wmt19-en-de
