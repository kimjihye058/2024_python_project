from flask import Flask, render_template, request, jsonify  # Flask 웹 애플리케이션 및 API를 위한 라이브러리
import os
import google.generativeai as genai

app = Flask(__name__)  # Flask 애플리케이션 인스턴스 생성

# 환경 변수에서 API 키 가져오기
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key is None:
    raise ValueError("API key not found. Please set the 'GOOGLE_API_KEY' environment variable.")

# API 키로 genai 구성 설정
genai.configure(api_key=api_key)

# 모델 생성 설정
generation_config = {
    "temperature": 0.5,                 # 응답 다양성 줄이기
    "top_p": 0.85,                      # 확률적 범위 줄이기
    "top_k": 20,                        # 고려할 단어 수 줄이기
    "max_output_tokens": 1000,           # 응답 길이 줄이기
    "response_mime_type": "text/plain"  # 응답 형식: 일반 텍스트
}

# 모델 인스턴스 생성
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",     # 모델 이름
    generation_config=generation_config # 설정값 전달
)

# 대화 세션 시작
chat_session = model.start_chat(
    history=[]                         # 초기 대화 히스토리 설정
)

# 레시피 관련 질문인지 확인하는 함수
def is_recipe_related(question):
    recipe_keywords = ['레시피', '요리', '재료', '만드는 방법']  # 레시피 관련 키워드 목록
    return any(keyword in question for keyword in recipe_keywords)  # 질문에 키워드 포함 여부 확인

# 홈 페이지 경로
@app.route("/")
def home():
    return render_template("index.html")  # 홈 페이지 렌더링

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return jsonify({"response": "이 페이지는 GET 요청을 지원하지 않습니다. POST 요청을 사용하세요."})

    # POST 요청 처리
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "메시지가 비어 있습니다. 메시지를 입력해주세요."})

    if not is_recipe_related(user_input):
        return jsonify({"response": "죄송합니다. 요리 레시피 변환만 할 수 있습니다."})

    chat_session.history.append({"role": "user", "parts": [user_input]})
    response = chat_session.send_message(user_input)
    print("Chatbot Response:", response)  # 디버그용 출력
    return jsonify({"response": response.text})


# 애플리케이션 실행
if __name__ == "__main__":
    app.run(debug=True)  # 디버그 모드로 Flask 서버 실행
