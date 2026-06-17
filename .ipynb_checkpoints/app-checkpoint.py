import streamlit as st
from openai import OpenAI
from dotenv import dotenv_values
from pypdf import PdfReader
from docx import Document

env = dotenv_values(".env")
openai_client = OpenAI(api_key=env["OPENAI_API_KEY"])

# --- WYBÓR MODELU W PANELU BOCZNYM ---
st.sidebar.title("Ustawienia bota")
selected_model = st.sidebar.selectbox(
    "Wybierz model OpenAI:",
    options=["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
    index=0  # Domyślnie gpt-4o-mini
)

st.markdown(
    """
    <style>
        div[data-baseweb="select"] {
            cursor: pointer !important;
        }
        div[data-testid="stSelectbox"] svg {
            cursor: pointer !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title(":black_joker: GPT z OpenAI")

def read_uploaded_files(uploaded_files):
    documents_text = ""
    for file in uploaded_files:
        # TXT
        if file.type == "text/plain":
            text = file.read().decode("utf-8")
            documents_text += f"\n\n===== PLIK: {file.name} =====\n{text}"

        # PDF
        elif file.type == "application/pdf":
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            documents_text += f"\n\n===== PLIK: {file.name} =====\n{text}"

        # DOCX
        elif "word" in file.type:
            doc = Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            documents_text += f"\n\n===== PLIK: {file.name} =====\n{text}"
            
    return documents_text

# --- FUNKCJA DO PRZETWARZANIA PYTAŃ I PLIKÓW ---
def get_chatbot_reply(user_prompt, model_name, chat_history, documents_text):
    messages = [
        {
            "role": "system",
            "content": """
            Jesteś ekspertem od wszystkiego.
            Odpowiadasz jasno, rzeczowo i szczerze.
            Analizujesz również przesłane dokumenty.
            """
        }
    ]

    # Pobieramy historię BEZ ostatniej wiadomości użytkownika 
    messages.extend(chat_history[-21:-1] if len(chat_history) > 1 else [])

    if documents_text:
        current_message = f"Dokumenty użytkownika:\n{documents_text}\n\nPytanie użytkownika:\n{user_prompt}"
    else:
        current_message = user_prompt

    messages.append({
        "role": "user",
        "content": current_message
    })

    response = openai_client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=1000
    )

    return {
        "role": "assistant",
        "content": response.choices[0].message.content
    }

# Inicjalizacja stanu sesji
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "documents" not in st.session_state:
    st.session_state["documents"] = "" 

# --- KROK 1: Najpierw rezerwujemy miejsce na historię czatu na samej górze ---
chat_container = st.container()

# --- KROK 2: Formularz wpisywania wiadomości na samym dole skryptu ---
with st.form("chat_form", clear_on_submit=True):
    uploaded_files = st.file_uploader(
        "📎 Dodaj pliki",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True
    )
    prompt = st.text_input("O co chcesz spytać?")
    send_button = st.form_submit_button("Wyślij")

# --- KROK 3: Logika po kliknięciu wyślij ---
if send_button and prompt:
    # Przetworzenie plików
    if uploaded_files:
        st.session_state["documents"] = read_uploaded_files(uploaded_files)

    # Przygotowanie wiadomości użytkownika z załącznikami
    user_content = prompt
    if uploaded_files:
        files_info = "\n".join([f" *📎 Załadowano plik: {file.name}*" for file in uploaded_files])
        user_content = f"{prompt}\n\n{files_info}"
                
    # Zapisujemy do sesji
    st.session_state["messages"].append({"role": "user", "content": user_content})

    # Pobranie odpowiedzi od bota i zapis do sesji
    chatbot_message = get_chatbot_reply(
        prompt,
        selected_model,
        st.session_state["messages"],
        st.session_state["documents"]
    )
    st.session_state["messages"].append(chatbot_message)

# --- KROK 4: Renderowanie historii rozmowy w zarezerwowanym kontenerze ---
# Pętla wykonuje się ZAWSZE i rysuje CAŁĄ zawartość w jednym miejscu NAD formularzem
with chat_container:
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])