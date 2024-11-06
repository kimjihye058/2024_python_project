from flask import Flask, render_template, request, jsonify  # python app.py로 시작, 웹브라우저 http://127.0.0.1:5000
import os
import google.generativeai as genai

app = Flask(__name__)

# 환경 변수에서 API 키를 가져옵니다.
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key is None:
    raise ValueError("API key not found. Please set the 'GOOGLE_API_KEY' environment variable.")

# API 키를 사용하여 genai를 구성합니다.
genai.configure(api_key=api_key)

# 모델 생성 설정
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# 대화 세션 시작
chat_session = model.start_chat(
    history=[]
)

def is_recipe_related(question):
    recipe_keywords = ['레시피', '요리', '재료', '만드는 방법']
    return any(keyword in question for keyword in recipe_keywords)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if not is_recipe_related(user_input):
        return jsonify({"response": "죄송합니다. 요리 레시피 변환만 할 수 있습니다."})

    # 사용자의 메시지를 세션에 추가하고 응답을 생성합니다.
    chat_session.history.append({"role": "user", "parts": [user_input]})
    response = chat_session.send_message(user_input)

    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)
