# Chatbot de Ciberseguridad con IA y RAG

## Descripción

Este proyecto consiste en el desarrollo de un chatbot especializado en ciberseguridad basado en un modelo de lenguaje local y técnicas de Recuperación Aumentada por Generación (RAG, Retrieval-Augmented Generation).

El sistema permite responder preguntas relacionadas con conceptos de ciberseguridad utilizando una base de conocimiento propia y adaptando las respuestas según el nivel de conocimientos del usuario.

Este proyecto ha sido desarrollado como Trabajo Fin de Grado (TFG) del Grado en Ingeniería Informática.

## Características

- Modelo de lenguaje ejecutado localmente mediante Ollama.
- Uso de Llama 3 como modelo conversacional.
- Recuperación de información mediante RAG.
- Búsqueda semántica utilizando embeddings.
- Base de conocimiento personalizada.
- Adaptación automática de las respuestas para:
  - Usuario técnico.
  - Usuario no técnico.
- Interfaz gráfica desarrollada con Streamlit.

## Tecnologías utilizadas

- Python 3
- Streamlit
- Ollama
- Llama 3
- Sentence Transformers
- NumPy
- Requests
  
## Estructura del proyecto

chatbot_ciberseguridad/
│
├── app.py
├── requirements.txt
├── README.md
│
└── knowledge/
    ├── phishing.txt
    ├── malware.txt
    ├── ransomware.txt
    ├── wifi.txt
    ├── passwords.txt
    ├── mfa.txt
    └── siem.txt

## Funcionamiento

El funcionamiento del chatbot sigue las siguientes etapas:

1. El usuario selecciona su perfil (técnico o no técnico).
2. Introduce una pregunta sobre ciberseguridad.
3. La pregunta se transforma en un embedding.
4. Se calcula la similitud con los documentos de la base de conocimiento.
5. Se recuperan los documentos más relevantes.
6. Se construye un prompt utilizando el contexto recuperado.
7. Llama 3 genera una respuesta adaptada al perfil seleccionado.
8. La respuesta se muestra en la interfaz.

### 3. Instalar las dependencias

pip install -r requirements.txt

## Ejecución del proyecto

Con el entorno virtual activado ejecutar: streamlit run app.py

El navegador abrirá automáticamente la aplicación.

## Base de conocimiento

La carpeta **knowledge** contiene los documentos utilizados por el sistema RAG.

Actualmente incluye información sobre:

- Phishing
- Malware
- Ransomware
- Redes WiFi
- Contraseñas seguras
- Autenticación multifactor (MFA)
- Sistemas SIEM

Estos documentos son convertidos en embeddings para realizar búsquedas semánticas y recuperar el contexto más relevante para cada consulta.


## Adaptación por perfiles

El chatbot adapta automáticamente el lenguaje empleado según el perfil seleccionado.

### Usuario no técnico

- Lenguaje sencillo.
- Explicaciones claras.
- Recomendaciones prácticas.
- Evita tecnicismos.

### Usuario técnico

- Terminología especializada.
- Explicaciones más detalladas.
- Información técnica adicional.
- Buenas prácticas de ciberseguridad.


## Ejemplo de uso

**Pregunta:**

He recibido un correo sospechoso, ¿qué debo hacer?

**Perfil no técnico**

El chatbot explica cómo identificar un posible phishing y recomienda no abrir enlaces ni descargar archivos adjuntos.

**Perfil técnico**

Además de identificar el phishing, describe indicadores de compromiso, cabeceras del correo, validación SPF, DKIM y DMARC, así como medidas de contención.

## Requisitos

- Python 3.10 o superior
- Ollama
- Modelo Llama 3 descargado
- Conexión local con Ollama


## Autor

Inés Elena Gómez Olocz

Trabajo Fin de Grado

Grado en Ingeniería Informática

Universidad Alfonso X el Sabio (UAX)

Curso 2025–2026
