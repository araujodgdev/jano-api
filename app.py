from flask import Flask, request, jsonify
import google.generativeai as genai
import re

app = Flask(__name__)

genai.configure(api_key='AIzaSyCyuv6EWCKobuKwVvkA0s5AUqb4yxBliVY')

model = genai.GenerativeModel(
  model_name="tunedModels/jano-v2-vzxrel0vrro8",
  generation_config=genai.GenerationConfig(
    response_mime_type="text/plain"
  )
)

chat = model.start_chat(history=[])

@app.route("/api/question", methods=["POST"])
def get_response():
    data = request.get_json()
    question = data.get("question") 

    if not question:
        return jsonify({"error": "No question provided"}), 400

    tuned_question = f"Responda sem caracteres especiais e não retorne emoções em texto simples: {question}"
    answer = chat.send_message(tuned_question)

    pattern = r'[\\*&]'

    cleaned_text = re.sub(pattern, '', answer.text)

    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return jsonify({"response": cleaned_text})