from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
openai_api_key = os.getenv("AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10")

app = Flask(__name__)

@app.route('/generate_react', methods=['POST'])
def generate_react():
    data = request.json['data']  # Get the data to be passed into the prompt

    # Initialize OpenAI GPT-4 model
    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-4")

    prompt_template = PromptTemplate(
        input_variables=["file_data"],
        template="""
You are an AI assistant that helps developers build UI components.

Given the following data:

{file_data}

Generate a React component to display the data in a user-friendly table with sorting and filtering capabilities.

Provide only the code for the component, and ensure that it is optimized for performance.
"""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    response = chain.run(file_data=data)
    
    # Return the generated code
    return jsonify({"generated_code": response})

if __name__ == '__main__':
    app.run(debug=True)
