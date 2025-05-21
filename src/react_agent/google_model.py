from google.oauth2 import service_account
from langchain_google_genai import ChatGoogleGenerativeAI

# Correct scope for Gemini
SCOPES = ["https://www.googleapis.com/auth/generative-language"]
SERVICE_ACCOUNT_FILE = "D:/Zikra LLC/task1 updated/react-agent/langgraphagent-08f82a4cbca2.json"

# Create scoped credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Initialize the LangChain Google model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    credentials=credentials
)

# Example usage
response = llm.invoke("Hello, how can I help you?")
print(response.content)