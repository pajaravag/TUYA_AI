from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline

class LlamaQuery:
    """Clase para interactuar con el modelo Llama 3.2."""

    def __init__(self, model_id):
        """Inicializa la clase con el ID del modelo."""
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id)
        self.pipeline = pipeline("text-generation", model = self.model, tokenizer = self.tokenizer)
        self.local_llm = HuggingFacePipeline(pipeline = self.pipeline)

    def ask_llama(self, question, context):
        """Consulta el modelo Llama 3.2 usando el conocimiento extraído."""
        prompt = f"Basado en la siguiente información:\n\n{context}\n\nResponde la siguiente pregunta de forma clara y concisa:\n\n{question}"
        response = self.local_llm(prompt)
        return response