import bentoml
from transformers import AutoModelForCausalLM

bentoml.transformers.save_model(
    "sfeir_hivemind_llm",
    AutoModelForCausalLM.from_pretrained("StabilityAI/stablelm-tuned-alpha-7b"),
    signatures={"generate": {"batchable": False, "batch_dim": 0}},
)
