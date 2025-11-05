import streamlit as st
st.title('집에 보내줘 제발')
a=st.text_input('너 이름 뭐야?')
b=st.selectbox('어떤 음식 좋아해?',['알리오올리오','까르보나라','토마토스파게티'])
if st.button('인사말 생성'):
  st.info(a+', .. 반가워')
  st.warning(b+'를 좋아하는구나. 나도 뭐..')
  st.error('잘 지내보자')
  st.balloons()
