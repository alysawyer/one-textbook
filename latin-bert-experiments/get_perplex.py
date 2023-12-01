from transformers import AutoModelForMaskedLM, AutoTokenizer
import torch
import numpy as np

model_name = 'cointegrated/rubert-tiny'
model = AutoModelForMaskedLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def score(model, tokenizer, sentence):
    tensor_input = tokenizer.encode(sentence, return_tensors='pt')
    repeat_input = tensor_input.repeat(tensor_input.size(-1)-2, 1)
    mask = torch.ones(tensor_input.size(-1) - 1).diag(1)[:-2]
    masked_input = repeat_input.masked_fill(mask == 1, tokenizer.mask_token_id)
    labels = repeat_input.masked_fill( masked_input != tokenizer.mask_token_id, -100)
    with torch.inference_mode():
        loss = model(masked_input, labels=labels).loss
    return np.exp(loss.item())

print(score(sentence='London is the capital of Great Britain.', model=model, tokenizer=tokenizer)) 
# 4.541251105675365
print(score(sentence='London is the capital of South America.', model=model, tokenizer=tokenizer)) 
# 6.162017238332462