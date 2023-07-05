import bentoml
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b", trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    "tiiuae/falcon-7b",
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
    load_in_8bit=True,
    device_map="auto",
    quantization_config=BitsAndBytesConfig(
        llm_int8_enable_fp32_cpu_offload=True,
    ),
)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

bentoml.transformers.save_model("sfeir-hivemind-falcon-7b", pipeline=pipeline)
