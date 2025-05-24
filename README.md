# Chirp 🐦
A lightweight Twitter-like social media API built with Flask.

## 🚀 Features

- 🔐 JWT-based authentication (register/login)
- 📝 Post creation and global feed
- 👥 User follow/unfollow system
- 🧡 Like/unlike system
- 💬 Comment system
- 🧭 Personalized feed (only from followed users)
- 🧾 Profile bio and update support
- 📄 Pagination for posts and feeds

---

## 🛠 Technologies Used

- Flask + Flask-JWT-Extended
- SQLAlchemy + SQLite (can be switched to PostgreSQL)
- Flask-Migrate
- Python 3.10+

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/emirhan-erisen/chirp.git
cd chirp
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file:

```env
SECRET_KEY=supersecretkey
DATABASE_URL=sqlite:///chirp.db
```

### 5. Run migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Start the server

```bash
python run.py
```

---

## 🧪 API Endpoints

### Auth
- `POST /auth/register`
- `POST /auth/login`

### Posts
- `GET /posts/`
- `GET /posts/feed`
- `POST /posts/`
- `POST /posts/<id>/like`
- `POST /posts/<id>/unlike`

### Users
- `GET /users/<id>`
- `GET /users/me`
- `PATCH /users/me`
- `POST /users/follow/<id>`
- `POST /users/unfollow/<id>`

### Comments
- `POST /comments/`
- `GET /comments/<post_id>`

---

## 📌 Author

**Emirhan Erişen**  
💼 [LinkedIn](https://www.linkedin.com/in/emirhan-eri%C5%9Fen-088009368/)
📧 emirhanerisen12@gmail.com  
💻 [GitHub](https://github.com/emirhanerisen)

---

## 🐳 Want to Contribute?

Feel free to fork the repo and submit a PR.  
This project is open for collaboration and improvement.