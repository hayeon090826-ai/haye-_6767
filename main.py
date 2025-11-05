import streamlit as st
st.title('집에 보내줘 제발')
a=st.text_input('너 이름 뭐임?')
st.selectbox('어떤 음식 좋아해?',['알리오올리오','까르보나라','토마토스파게티'])
if st.button('인사말 생성'):
  st.write(a+'님, ㅎㅇ. 반갑')
