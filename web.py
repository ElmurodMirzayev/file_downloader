import streamlit as st
import os
import json
import uuid
from datetime import datetime

# ----------------------------
# Настройки
# ----------------------------
UPLOAD_FOLDER = "storage"
DATA_FILE = "files.json"

# Создать папку если нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Создать json если нет
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)


# ----------------------------
# Функции
# ----------------------------
def load_files():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_files(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def format_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size / (1024 * 1024):.2f} MB"


# ----------------------------
# Интерфейс
# ----------------------------
st.set_page_config(page_title="Файловое хранилище", page_icon="📁")

st.title("📁 Файловое хранилище")
st.write("Загружай файлы и скачивай их позже.")

# ----------------------------
# Загрузка файлов
# ----------------------------
uploaded_files = st.file_uploader(
    "Выберите файлы",
    accept_multiple_files=True
)

if st.button("Загрузить"):
    if uploaded_files:
        files_data = load_files()

        for uploaded_file in uploaded_files:
            file_id = str(uuid.uuid4())
            filename = uploaded_file.name
            filepath = os.path.join(UPLOAD_FOLDER, file_id + "_" + filename)

            # Сохранение файла
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Добавление информации
            files_data.append({
                "id": file_id,
                "name": filename,
                "path": filepath,
                "size": uploaded_file.size,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        save_files(files_data)
        st.success("Файлы успешно загружены!")
        st.rerun()
    else:
        st.warning("Сначала выберите файл.")

# ----------------------------
# Список файлов
# ----------------------------
st.subheader("📂 Список файлов")

files_data = load_files()

if not files_data:
    st.info("Файлов пока нет.")
else:
    for file in files_data[::-1]:
        col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

        with col1:
            st.write(file["name"])

        with col2:
            st.write(format_size(file["size"]))

        with col3:
            st.write(file["date"])

        with col4:
            if os.path.exists(file["path"]):
                with open(file["path"], "rb") as f:
                    st.download_button(
                        label="⬇",
                        data=f,
                        file_name=file["name"],
                        key=file["id"]
                    )