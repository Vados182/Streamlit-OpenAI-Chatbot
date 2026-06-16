# 🃏 GPT z OpenAI — Multimedialny Asystent Chatbot
Aplikacja webowa typu Chatbot zbudowana w języku Python z wykorzystaniem biblioteki Streamlit oraz oficjalnego API OpenAI. Projekt umożliwia interaktywną konwersację z zaawansowanymi modelami językowymi (LLM) oraz posiada funkcję analizy kontekstowej przesyłanych dokumentów (prostego mechanizmu RAG/In-Context Learning).

## 🚀 Kluczowe Funkcje
Wybór Modelu w Czasie Rzeczywistym: Możliwość dynamicznej zmiany modelu z poziomu panelu bocznego (sidebar). Obsługiwane modele: gpt-4o-mini, gpt-4o, gpt-4-turbo oraz gpt-3.5-turbo.

Multiformatowe Przetwarzanie Dokumentów: Bot potrafi czytać, łączyć i analizować treść z wielu plików jednocześnie. Obsługuje formaty:

PDF (z użyciem pypdf)

DOCX (z użyciem python-docx)

TXT (standardowe kodowanie UTF-8)

Zarządzanie Historią Czatu: Aplikacja utrzymuje kontekst rozmowy w ramach aktywnej sesji użytkownika (st.session_state), przesyłając do API historię ostatnich wiadomości (bufor pamięci do 20 wpisów wstecz).

Intuicyjny Interfejs (UX): Wykorzystanie formularza Streamlit (st.form) z automatycznym czyszczeniem pola tekstowego po wysłaniu wiadomości oraz dynamiczne renderowanie historii rozmowy powyżej formularza wejściowego.

Customowe Style CSS: Subtelne modyfikacje interfejsu (np. zmiana kursora na pointer dla elementów typu selectbox) podnoszące estetykę aplikacji.