from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch


baseModel = "TinyLlama/TinyLlama-1.1B-Chat-v0.3"
# Load base model
tokenizer = AutoTokenizer.from_pretrained(baseModel)

model = AutoModelForCausalLM.from_pretrained(baseModel)
model.to("cuda" if torch.cuda.is_available() else "cpu")
special_tokens = ["### Instruction:", "### Response:"]
tokenizer.add_tokens(special_tokens)
model.resize_token_embeddings(len(tokenizer))

def parse_intent(prompt: str) -> str:
    input_text = f"### Instruction:\n{prompt}\n\n### Response:"
    inputs = tokenizer(input_text, return_tensors="pt", max_length=2048, truncation=True).to(model.device)

    # Enable sampling for more creative/longer responses
    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,  # Only controls *new* generated tokens
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        eos_token_id=tokenizer.eos_token_id,  # Make sure this is defined
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("### Response:")[-1].strip()
