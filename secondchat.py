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

def is_recipe_related(question):
    # 질문이 레시피와 관련이 있는지 확인하는 간단한 체크 (예: 키워드 포함)
    recipe_keywords = ['레시피', '요리', '재료', '만드는 방법']
    return any(keyword in question for keyword in recipe_keywords)

def is_conversion_related(question):
    # 질문이 변환과 관련이 있는지 확인하는 체크
    return "변환" in question

def chat_with_bot():
    print("=====================================================")
    print("레시피 변환기 챗봇에 오신 것을 환영합니다!")
    print("먹고싶은 요리 레시피를 말씀해주세요!")
    print("-----------------------------------------------------")
    print("**주의사항**")
    print("1. 기존 레시피 이름을 ['레시피']라는 키워드와 함께 입력해주세요.")
    print("예) OOO 레시피를 알려주세요.")
    print("2. 본인의 식단 유형을 ['변환']이라는 키워드와 함께 입력해주세요.")
    print("예) 저는 비건입니다. 레시피를 변환해주세요.")
    print("3. 채팅 중 종료를 원하신다면 [종료]나 [exit]를 입력해주세요.")
    print("=====================================================")
    
    # 질문 체크 여부
    first_question = True
    second_question = True

    while True:
        user_input = input("사용자: ")
        if user_input.lower() in ['종료', 'exit']:
            print("챗봇을 종료합니다.")
            break

        # 첫 질문일 경우 레시피 관련 체크
        if first_question:
            if not is_recipe_related(user_input):
                print("챗봇: 죄송합니다. 요리 레시피 변환만 할 수 있습니다.")
                continue
            first_question = False  # 첫 질문 체크 후 변경
            second_question = True  # 두 번째 질문 체크 가능

        # 사용자의 메시지를 세션에 추가합니다.
        chat_session.history.append({"role": "user", "parts": [user_input]})

        # 챗봇의 응답을 생성합니다.
        response = chat_session.send_message(user_input)

        # 응답 텍스트 출력
        print(f"챗봇: {response.text}")

        # 레시피 관련 질문 후 안내 메시지 추가
        if first_question is False and second_question is True:
            print("챗봇: 당신의 식단유형을 알려주세요.")
            second_question = False  # 두 번째 질문 체크 후 변경

# 챗봇과 대화 시작
chat_with_bot()
