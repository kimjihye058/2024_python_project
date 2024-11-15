# 단순 콘솔 출력

import os
import google.generativeai as genai

# 환경 변수에서 API 키 가져오기
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key is None:
    raise ValueError("API key not found. Please set the 'GOOGLE_API_KEY' environment variable.")

# API 키로 genai 구성 설정
genai.configure(api_key=api_key)

# 모델 생성 설정
generation_config = {
    "temperature": 1,                  # 창의성 조절 (높을수록 다양)
    "top_p": 0.95,                     # 상위 확률 95% 단어만 선택
    "top_k": 40,                       # 상위 40개 단어만 고려
    "max_output_tokens": 8192,         # 최대 출력 토큰 제한
    "response_mime_type": "text/plain" # 응답 형식: 일반 텍스트
}

# 모델 인스턴스 생성
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",     # 사용할 모델 이름
    generation_config=generation_config, # 설정값 전달
)

# 대화 세션 초기화
chat_session = model.start_chat(
    history=[]                         # 초기 히스토리 빈 리스트
)

# 챗봇과 대화할 함수 정의
def chat_with_bot():
    print("레시피 변환기 챗봇에 오신 것을 환영합니다!")  # 환영 메시지 출력
    while True:
        user_input = input("사용자: ")  # 사용자 입력 받기
        if user_input.lower() in ['종료', 'exit']:  # '종료' 또는 'exit' 입력 시 종료
            print("챗봇을 종료합니다.")
            break

        # 사용자의 메시지를 히스토리에 추가
        chat_session.history.append({"role": "user", "parts": [user_input]})

        # 챗봇 응답 생성
        response = chat_session.send_message(user_input)

        # 챗봇 응답 출력
        print(f"{response.text}")

# 챗봇과 대화 시작
chat_with_bot()  # 함수 호출로 챗봇 실행
