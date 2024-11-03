import os
import google.generativeai as genai

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

def chat_with_bot():
    print("레시피 변환기 챗봇에 오신 것을 환영합니다!")
    while True:
        user_input = input("사용자: ")
        if user_input.lower() in ['종료', 'exit']:
            print("챗봇을 종료합니다.")
            break

        # 사용자의 메시지를 세션에 추가합니다.
        chat_session.history.append({"role": "user", "parts": [user_input]})

        # 챗봇의 응답을 생성합니다.
        response = chat_session.send_message(user_input)

        # 응답 텍스트 출력
        print(f"{response.text}")

# 챗봇과 대화 시작
chat_with_bot()
