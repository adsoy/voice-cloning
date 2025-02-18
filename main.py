import streamlit as st
from streamlit_mic_recorder import mic_recorder
import os
import replicate
from io import BytesIO

st.set_page_config(page_title='Ses Klonlama Uygulaması', page_icon='🎙️')
t1, t2, t3 = st.columns([1.2,2,1])
with t2:
    st.title('Sesini Klonla 🎙️')


url = "https://replicate.com/account/api-tokens"

st.markdown("""Bu uygulama ses klonlama için **xtts-v2** modelini kullanıyor.
        Yani bu uygulama (veya modeli) kullanarak **İngilizce, Fransızca,
        İspanyolca, Rusça** dahil olmak üzere 10'dan fazla dilde konuşabilirsiniz.""")

st.markdown("""Başlamak için aşağıdaki "**Kaydı Başlat**" düğmesine basarak sesinizi kaydedebilir, daha sonra 
            ekranda çıkan metin kutusuna konuşmak istediğiniz metni girin ve konuşmak istediğiniz dili seçin.
             Son olarak [Replicate](%s) hesabı açıp API key alın ve sesi klonla düğmesine basın🔥""" % url)


st.markdown("X'te bana ulaşın: [**:blue[Giray]**](https://twitter.com/gryhkn)")
st.divider()

col1, col2, col3 = st.columns([2,2,1])

with col2:
    audio = mic_recorder(start_prompt="⏺️ Kaydı Başlat", stop_prompt="⏹️ Kaydı Durdur", key='recorder')

if audio:
    st.audio(audio['bytes'])

    audio_buffer = BytesIO(audio['bytes'])

    st.download_button(
        label="Kaydı İndir",
        data=audio['bytes'],
        file_name="kayit.wav",
        mime="audio/wav"
    )

    user_text = st.text_area("Seslendirmek istediğiniz metni buraya girin:")


    if user_text:

        language = st.selectbox("Hedef dil seçiniz",
                                ('en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh', 'hu', 'ko'))
        replicate_api_key = st.text_input("Replicate API Key:", type="password")

        if replicate_api_key:
            os.environ["REPLICATE_API_TOKEN"] = replicate_api_key

        if st.button('Sesi Klonla') and replicate_api_key:
            print("REPLICATE_API_TOKEN: ", replicate_api_key)
            with st.spinner('Ses klonlanıyor...'):
                audio_bytes_io = BytesIO(audio['bytes'])

                output = replicate.run(
                    "lucataco/xtts-v2:6b2385a9c081443f17041bf1a4caeb36393903f4d7e94468f32e90b2ec57ffc2",
                    input={
                             "text": user_text,
                             "speaker": audio_bytes_io,
                             "language": language,
                             "cleanup_voice": False
                    }
                )

                if output:
                    audio_uri = output
                    st.audio(audio_uri, format='audio/wav')
                    st.download_button('Sesi İndir', audio_uri, file_name='cloned_voice.wav')
