# test_gemini.py
from langchain.chat_models import init_chat_model

model = init_chat_model("gemini-pro", model_provider="google_vertexai")

response = model.invoke("What's the weather like on Mars?")
print(response)
