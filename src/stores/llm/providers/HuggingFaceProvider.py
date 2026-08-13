# from sentence_transformers import SentenceTransformer
# from transformers import pipeline
# from ..LLMInterface import LLMInterface
# import logging


# class HuggingFaceProvider(LLMInterface):

#     def __init__(
#         self,
#         default_input_max_characters=1000,
#         default_generation_max_output_tokens=1000,
#         default_generation_temperature=0.1,
#     ):

#         self.default_input_max_characters = default_input_max_characters
#         self.default_generation_max_output_tokens = default_generation_max_output_tokens
#         self.default_generation_temperature = default_generation_temperature

#         self.embedding_model = None
#         self.generation_model = None

#         self.embedding_model_id = None
#         self.generation_model_id = None

#         self.logger = logging.getLogger(__name__)

#     def process_text(self, text: str):
#         return text[: self.default_input_max_characters].strip()

#     #######################################################
#     # Embeddings
#     #######################################################

#     def set_embedding_model(self, model_id: str, embedding_size: int = None):
#         self.embedding_model_id = model_id
#         self.embedding_model = SentenceTransformer(model_id)

#     def embed_text(self, text: str, document_type: str = None):

#         if self.embedding_model is None:
#             self.logger.error("Embedding model is not initialized")
#             return None

#         embedding = self.embedding_model.encode(
#             self.process_text(text),
#             convert_to_numpy=True,
#             normalize_embeddings=True,
#         )

#         return embedding.tolist()

#     #######################################################
#     # Generation
#     #######################################################

#     def set_generation_model(self, model_id: str):

#         self.generation_model_id = model_id

#         self.generation_model = pipeline(
#             "text-generation",
#             model=model_id,
#         )

#     def generate_text(
#         self,
#         prompt: str,
#         chat_history=[],
#         max_output_tokens=None,
#         temperature=None,
#     ):

#         if self.generation_model is None:
#             self.logger.error("Generation model is not initialized")
#             return None

#         max_output_tokens = (
#             max_output_tokens
#             if max_output_tokens
#             else self.default_generation_max_output_tokens
#         )

#         temperature = (
#             temperature
#             if temperature
#             else self.default_generation_temperature
#         )

#         output = self.generation_model(
#             self.process_text(prompt),
#             max_new_tokens=max_output_tokens,
#             temperature=temperature,
#             do_sample=True,
#         )

#         return output[0]["generated_text"]

#     #######################################################

#     def construct_prompt(self, prompt: str, role: str):
#         return {
#             "role": role,
#             "text": self.process_text(prompt),
#         }