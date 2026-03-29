from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(context, question):
    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content