# Social Network Website (HW6)

This project is a Django-based **nano-blogging social network** built as part of Homework 6 for the Web Application Development course. It extends earlier assignments to include **AJAX functionality**, enabling real-time interactions without full page reloads.

---

## 🚀 Features
- **User Authentication**
  - Registration, login, and logout flows with form validation:contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}.
- **Profile Management**
  - Editable profile page with bio and profile picture:contentReference[oaicite:2]{index=2}.
  - Ability to follow and unfollow other users.
- **Posting & Streams**
  - Users can create posts that appear in:
    - **Global Stream**: all users’ posts:contentReference[oaicite:3]{index=3}.
    - **Follower Stream**: posts only from users you follow:contentReference[oaicite:4]{index=4}.
- **Comments via AJAX**
  - Add comments under posts without reloading the page:contentReference[oaicite:5]{index=5}.
  - Comments show author, timestamp, and are displayed in chronological order:contentReference[oaicite:6]{index=6}.
- **Auto-Refreshing Streams**
  - Global and follower streams refresh every 5 seconds via AJAX, pulling the latest posts and comments:contentReference[oaicite:7]{index=7}.
- **Error Handling**
  - Robust server-side validation ensures invalid inputs or unauthorized requests return proper JSON error codes (400/401/403/405):contentReference[oaicite:8]{index=8}.

---

## 🛠️ Tech Stack
- **Backend:** Django (Python):contentReference[oaicite:9]{index=9}
- **Frontend:** HTML5, CSS, Django Templates
- **AJAX / JS:** JavaScript for dynamic updates (fetching posts/comments, submitting comments)
- **Database:** SQLite (default Django configuration)
- **Version Control:** Git & GitHub
