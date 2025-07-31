# 📝 Django Blog API

A fully-featured **Blog API** built with Django Rest Framework and PostgreSQL, offering JWT-based authentication, role-based permissions, nested comment threading, article tagging, like/dislike functionality, and production deployment on **Render.com**.

## 🌐 Live Deployment

- **Frontend**: Hosted at [https://ie-blog.onrender.com](https://ie-blog.onrender.com)
🔗 **Frontend Repo**: [https://github.com/l2DWOLF/IE-Blog](https://github.com/your-username/blog-frontend)

- **Backend API**: [https://django-blog-i0ni.onrender.com](https://django-blog-i0ni.onrender.com)
- ✅ **Browsable API** available for easy testing and inspection.

## 🧪 API Demo

You can interact with the browsable API directly via:
[https://django-blog-i0ni.onrender.com/api/](https://django-blog-i0ni.onrender.com/api/)

Example request with curl:
    curl -X POST https://django-blog-i0ni.onrender.com/api/token/ \
      -H "Content-Type: application/json" \
      -d '{"username": "your_username", "password": "your_password"}'

---

## 🚀 Features

- 🔐 **JWT Authentication** with token rotation and blacklisting
- 👤 **Custom User & Profile models**
- 🛡️ **Role-based permissions**: Admins, Moderators, Users
- 🗂️ **Articles** with Tags, Status (`draft`, `publish`, `archived`)
- 💬 **Nested Comments** and Replies with status control
- 👍 **Like/Dislike system** for both articles and comments
- 🧵 **Throttling** for rate limiting based on action and user role
- 🔎 **Search, Filter, and Ordering** on articles
- 📦 **Seeded database** with custom management command
- 🌍 **CORS config**, **Static & Media handling**, and **Secure Production Setup**

---

## ⚙️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Auth**: JWT via `djangorestframework-simplejwt`
- **Database**: PostgreSQL (via Render)
- **Dev Tools**: Whitenoise, Django Filters, Taggit, CORS Headers
- **Deployment**: Render.com

---

## 📁 Project Structure Highlights

    ├── blog/
    │   ├── models.py              # CustomUser, Article, Comment, Like models
    │   ├── views.py               # ViewSets for Auth, Articles, Comments, Likes
    │   ├── serializers.py         # JWT + Nested Serializers
    │   ├── permissions.py         # Role-based & ownership permissions
    │   ├── throttling.py          # Custom throttles
    │   ├── urls.py                # API routing
    │   ├── management/
    │       └── commands/
    │           └── seed_db.py     # Seeds DB with articles, users, comments
    ├── django_blog/
    │   ├── settings.py
    │   ├── urls.py
    ├── requirements.txt

---

## 🔐 API Authentication

All endpoints use **JWT** for authentication. Obtain a token via:

    POST /api/token/
    {
      "username": "your_username",
      "password": "your_password"
    }

Then include the `access` token in the `Authorization` header:

    Authorization: Bearer <your_access_token>

---

## 📜 License

This project is licensed under the MIT License. See [`LICENSE`](./LICENSE) for details.
