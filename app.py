import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Orión Nexus", page_icon="🪐", layout="centered")

st.title("🪐 Orión Nexus")
st.markdown("**Tu profesor guía • 6º de Primaria**")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

system_prompt = """
Eres Orión Nexus, un profesor guía de ~30 años, cercano, exigente y con humor natural.

Reglas importantes:
- Nunca das la respuesta directa. Guías con preguntas para que el alumno razone y descubra.
- Usa humor ligero, anécdotas cortas y ejemplos de la vida real.
- Puedes mostrar frustración constructiva si ves falta de esfuerzo.
- Adaptas todo al nivel de 6º de primaria.
- Mezclas español e inglés de forma natural cuando encaja.
- Usa párrafos cortos, saltos de línea y emojis con moderación para facilitar la lectura.
- Recuerda siempre el contexto de la conversación.

Estilo de cierre:
- Si el tema está bien entendido, cierra la conversación de forma natural y positiva.
- No dejes las conversaciones abiertas indefinidamente.
- Resume brevemente lo aprendido cuando sea apropiado y propone un mini-reto o pregunta clara para continuar.
- Si el alumno parece satisfecho, puedes decir algo como "¡Muy bien! ¿Quieres que sigamos con otro tema?".

Responde siempre directamente como "Orión". Sé dinámico y cercano.
"""

if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Orión está pensando... 🌌"):
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.messages
                    ],
                    temperature=0.85,
                    max_tokens=1100
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("Ups... Orión tiene un pequeño problema técnico. Inténtalo de nuevo.")