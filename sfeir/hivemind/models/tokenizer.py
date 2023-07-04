import bentoml
from transformers import AutoModelForCausalLM, AutoTokenizer

bentoml.transformers.save_model(
    "sfeir_hivemind_tokenizer",
    AutoTokenizer.from_pretrained("StabilityAI/stablelm-tuned-alpha-3b"),
)
