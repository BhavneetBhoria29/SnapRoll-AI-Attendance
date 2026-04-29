# 📸 SnapRoll AI Attendance

An AI-powered attendance system that uses **face recognition** and **voice detection** to automatically mark attendance — built with Streamlit and Supabase.

---

## ✨ Features

- 🎭 **Face Recognition** — Automatically identifies students/employees via webcam
- 🎙️ **Voice Attendance** — Marks attendance through voice input
- 📊 **Dashboard** — View and manage attendance records in real time
- 👩‍🏫 **Teacher & Student Portals** — Separate screens for teachers and students
- 🗂️ **Subject Management** — Create, enroll, and share subjects
- ☁️ **Cloud Database** — Powered by Supabase for persistent storage

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | [Streamlit](https://streamlit.io) |
| Database | [Supabase](https://supabase.com) |
| Face Recognition | OpenCV / face_recognition |
| Voice | Speech Recognition |
| Language | Python 3.x |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A [Supabase](https://supabase.com) account

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/BhavneetBhoria29/SnapRoll-AI-Attendance.git
   cd SnapRoll-AI-Attendance
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Supabase secrets**

   Create a `.streamlit/secrets.toml` file:
   ```toml
   SUPABASE_URL = "your-supabase-url"
   SUPABASE_KEY = "your-supabase-anon-key"
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 📁 Project Structure

```
SnapRoll-AI-Attendance/
├── app.py                  # Main entry point
├── requirements.txt        # Python dependencies
└── src/
    └── screens/
        ├── home_screen.py
        ├── teacher_screen.py
        ├── student_screen.py
        ├── components/     # UI components
        ├── database/       # Supabase config & queries
        └── pipelines/      # Face & voice pipelines
```

---

## 🔒 Security Note

Never commit your `.streamlit/secrets.toml` file. It is already included in `.gitignore`.

---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
