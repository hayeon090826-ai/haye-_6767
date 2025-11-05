import streamlit as st
st.title('집에 보내줘 제발')
a=st.text_input('너 이름 뭐임?')
if st.button('인사말 생성'):
  st.write(a+'님, ㅎㅇ. 반감')
