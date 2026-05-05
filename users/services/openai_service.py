from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.API_KEY)

def get_ai_response(user_message):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content
