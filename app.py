import streamlit as st
import requests
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

KNOWLEDGE_DIR = Path("knowledge")


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


embedding_model = load_embedding_model()


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def load_knowledge():
    docs = []
    if KNOWLEDGE_DIR.exists():
        for file in KNOWLEDGE_DIR.glob("*.txt"):
            try:
                content = file.read_text(encoding="utf-8")
                embedding = embedding_model.encode(content)

                docs.append({
                    "filename": file.name,
                    "content": content,
                    "embedding": embedding
                })
            except Exception as e:
                st.warning(f"No se pudo leer {file.name}: {e}")
    return docs


def retrieve_context(user_query, docs, max_docs=2):
    if not docs:
        return "No hay documentos en la base de conocimiento."

    query_embedding = embedding_model.encode(user_query)
    scored_docs = []

    for doc in docs:
        score = cosine_similarity(query_embedding, doc["embedding"])
        scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_docs = scored_docs[:max_docs]

    context = "\n\n".join(
        [
            f"Documento: {doc['filename']}\n"
            f"Similitud: {score:.3f}\n"
            f"{doc['content']}"
            for score, doc in top_docs
        ]
    )
    return context


def build_prompt(profile, user_query, context):
    if profile == "No técnico":
        system_style = (
            "Eres un asistente de ciberseguridad para usuarios no técnicos. "
            "Responde con lenguaje claro, sencillo y práctico. "
            "Evita jerga innecesaria. "
            "Explica el riesgo de forma comprensible y da 4 pasos concretos. "
            "No inventes información. Si no estás seguro, dilo claramente. "
            "Responde en un máximo de 7 frases."
        )
    else:
        system_style = (
            "Eres un asistente de ciberseguridad para usuarios técnicos. "
            "Responde con precisión técnica y terminología adecuada. "
            "Incluye análisis, riesgo, mitigación y buenas prácticas cuando sea útil. "
            "No inventes información. Si no estás seguro, dilo claramente. "
            "Responde de forma breve, en un máximo de 5 frases o 5 puntos cortos."
        )

    full_prompt = f"""
{system_style}

Contexto recuperado mediante embeddings:
{context}

Pregunta del usuario:
{user_query}

Instrucciones:
- Usa el contexto si es relevante.
- Adapta la respuesta al perfil del usuario.
- Si el contexto no basta, responde con prudencia.
- No des instrucciones ofensivas ni peligrosas.
- Responde siempre en español.
"""
    return full_prompt


def generate_answer(prompt):
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3:latest",
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()
    data = response.json()
    return data["response"]


st.set_page_config(page_title="Chatbot de Ciberseguridad TFG", page_icon="🛡️")

# Estado inicial
if "profile_selected" not in st.session_state:
    st.session_state.profile_selected = False

if "profile" not in st.session_state:
    st.session_state.profile = None


# =========================
# PANTALLA 1: SELECCIÓN DE USUARIO
# =========================

if not st.session_state.profile_selected:

    st.markdown(
        """
        <div style='text-align: center; padding-top: 60px;'>
            <h1>🛡️ Chatbot de Ciberseguridad</h1>
            <p style='font-size: 20px; color: #555;'>
                Selecciona el tipo de usuario para adaptar la respuesta del sistema.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style='
                padding: 25px;
                border-radius: 15px;
                background-color: #f1f5f9;
                text-align: center;
                border: 1px solid #d0d7de;
            '>
                <h3>👤 Usuario no técnico</h3>
                <p>Explicaciones sencillas, claras y prácticas.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Entrar como No técnico", use_container_width=True):
            st.session_state.profile = "No técnico"
            st.session_state.profile_selected = True
            st.rerun()

    with col2:
        st.markdown(
            """
            <div style='
                padding: 25px;
                border-radius: 15px;
                background-color: #f1f5f9;
                text-align: center;
                border: 1px solid #d0d7de;
            '>
                <h3>🧑‍💻 Usuario técnico</h3>
                <p>Respuestas con mayor detalle y terminología técnica.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Entrar como Técnico", use_container_width=True):
            st.session_state.profile = "Técnico"
            st.session_state.profile_selected = True
            st.rerun()


# =========================
# PANTALLA 2: CHATBOT
# =========================

else:

    st.title("🛡️ Chatbot de Ciberseguridad")

    st.write(
        "Prototipo mínimo para usuarios técnicos y no técnicos, "
        "basado en un modelo local con Ollama y recuperación semántica mediante embeddings."
    )

    st.info(f"Perfil seleccionado: **{st.session_state.profile}**")

    if st.button("Cambiar perfil"):
        st.session_state.profile_selected = False
        st.session_state.profile = None
        st.rerun()

    user_query = st.text_area(
        "Escribe tu consulta:",
        placeholder="Ejemplo: He recibido un correo sospechoso, ¿puede ser phishing?"
    )

    if st.button("Enviar consulta"):
        if not user_query.strip():
            st.warning("Escribe una consulta antes de enviar.")
        else:
            docs = load_knowledge()
            context = retrieve_context(user_query, docs, max_docs=2)
            prompt = build_prompt(st.session_state.profile, user_query, context)

            with st.spinner("Generando respuesta..."):
                try:
                    answer = generate_answer(prompt)

                    st.subheader("Respuesta del sistema")
                    st.write(answer)

                    with st.expander("Contexto recuperado mediante embeddings"):
                        st.text(context)

                except requests.exceptions.Timeout:
                    st.error("Ollama tardó demasiado en responder.")
                except requests.exceptions.ConnectionError:
                    st.error(
                        "No se pudo conectar con Ollama. "
                        "Asegúrate de que Ollama está instalado y ejecutándose."
                    )
                except Exception as e:
                    st.error(f"Error al generar la respuesta: {e}")