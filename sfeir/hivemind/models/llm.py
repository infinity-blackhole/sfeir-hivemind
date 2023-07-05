import bentoml
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b", trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    "tiiuae/falcon-7b",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    load_in_8bit=True,
    device_map="auto",
)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

bentoml.transformers.save_model("sfeir-hivemind-falcon-7b", pipeline)
