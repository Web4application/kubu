import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

async def query_llm(message: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a helpful project assistant."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM error: {str(e)}"
