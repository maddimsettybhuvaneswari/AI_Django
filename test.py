# from google import genai

# client = genai.Client(api_key="YOUR_API_KEY")

# try:
#     response = client.models.generate_content(
#         model="gemini-1.5-flash-latest",
#         contents="Hello"
#     )
#     print("SUCCESS:", response.text)
# except Exception as e:
#     print("ERROR:", e)
from google import genai

client = genai.Client(api_key="AIzaSyD073S5__ekvktaZDhYkrzXtFN1_gYYYUc")

models = client.models.list()

for m in models:
    print(m.name)
