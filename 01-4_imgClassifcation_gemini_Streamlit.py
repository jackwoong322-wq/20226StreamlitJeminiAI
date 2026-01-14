import os
from PIL import Image
import google.genai as genai
#from dotenv import load_dotenv

# - 0)  라이브러리 추가하기 : streamlit
import streamlit as st

# client 객체의 models.generate_content 사용
def classify_image(client, prompt, image, model):
    response = client.models.generate_content(
        model=model,
        contents=[prompt, image]
    )
    return response.text

def streamlit_app(client, prompt: str):
    st.set_page_config(
                        page_title="Ex-stream-ly Cool App",
                        page_icon="🧊",
                        layout="wide",
                        initial_sidebar_state="expanded"
                        )
    st.title("이미지 분류기 - OpenAI")

    # - 2) prompt 작성하기 : st.text_area
    with st.sidebar:
        model = st.selectbox(
            "모델 선택",
            options=['gemini-2.5-flash-lite', "gemini-3-flash-preview", "gemini-3-flash"],
            index=0,
        )
    prompt = st.text_area('프롬프트 입력',value=prompt, height = 200)

    # - 3) 이미지 업로기하기 : st.file_uploader
    upload_file = st.file_uploader("이미지 업로드", type= ["png", "jpg", "jpeg"])

    # - 4) 업로드한 이미지 보여주기 : st.image
    if upload_file:
        img = Image.open(upload_file)
        st.image(img, caption= '업로드한 이미지', width='stretch')

    response = None
    # - 5) 분류 실행하기 : st.button / st.spinner
    if img is None:
        st.warning("이미지를 업로드해주세요.")
    else:
        if st.button("분류 실행"):
            with st.spinner('분류 중...'):
                response = classify_image(client, prompt, img, model=model)

    # - 6) 결과 출력하기 : st.write / st.code
    st.subheader('분류 결과')
    if response:
     st.code(response)
    else :
     st.write("아직 분류 결과가 없습니다. 이미지를 업로드하고 '분류 실행' 버튼을 눌러주세요.")  

def main():
    #load_dotenv()

    # 1. 클라이언트 생성 (API 키 설정)
    client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
    
    # GPT에게 보낼 프롬프트 정의
    prompt = """
    영상을 보고 다음 보기 내용이 포함되면 1, 포함되지 않으면 0으로 분류해줘.
    보기 = [건축물, 바다, 산]
    JSON format으로 키는 'building', 'sea', 'mountain'으로 하고 각각 건축물, 바다, 산에 대응되도록 출력해줘.
    자연 이외의 건축물이 조금이라도 존재하면 'building'을 1로, 물이 조금이라도 존재하면 'sea'을 1로, 산이 조금이라도 보이면 'mountain'을 1로 설정해줘.
    markdown format은 포함하지 말아줘.
    """
    
    streamlit_app(client, prompt)

if __name__ == "__main__":
    main()