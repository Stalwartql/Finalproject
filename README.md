ZenStudy 📚
ZenStudy is a web-based study planner and productivity application developed using Python and Streamlit. 
The project was inspired by an earlier university project (“BookExploring”) and expanded into a more advanced, feature-rich tool designed to support users in managing their study workflow efficiently.

🌐 👉 https://zenstudy.streamlit.app/

📌 About
ZenStudy was developed as part of a university project and extended into a comprehensive productivity application. 
It demonstrates practical experience in building full-stack data-driven applications, integrating external APIs, and designing user-focused features.

🚀 Features
Study Planner – Manage tasks, deadlines, and priorities
Productivity Tracker – Monitor study progress
Pomodoro Timer – Improve focus using time management techniques
QR Code Generator – Generate QR codes for quick access
International Book Explorer – Discover books globally
User Authentication System – Secure login and registration
Personal Account Page – View user information securely

🛠️ Tech Stack
Python
Streamlit
MongoDB
Pandas
External APIs:
Unsplash (image search)
Spotify (music integration)
Hugging Face (chatbot functionality)

🧩 Project Structure
The application is built using a modular structure:
studyplanner.py – Main application logic and UI
auth.py – Handles user authentication and MongoDB connection
unsplashAPI.py – Handles image search functionality

The app consists of multiple pages and components:
Home Page (user introduction)
Navigation Page (access to all features)
Login/Register Page
Account Page (visible after login)

Session state is used extensively to manage:
User authentication status
Page navigation
Feature-specific interactions
🔐 Authentication & Security
User registration and login system
User data stored in MongoDB
Passwords displayed securely (masked)
Session-based authentication using Streamlit session state
Logout functionality clears session data
⚙️ Development Process

The project followed a structured and iterative approach:
Defined core features and application structure
Built core functionalities step by step
Implemented session management for dynamic behavior
Integrated external APIs
Refined UI based on user feedback

Each feature was developed as an independent module, making the code easier to maintain and debug.

👥 User Feedback

User testing provided valuable insights:

Positive feedback on:
Intuitive interface
Integration of multiple productivity tools
Personalized account page
Suggested improvements:
Better layout and spacing
Improved sidebar design
More refined positioning of features
🔮 Future Improvements
Enhanced UI/UX design
Dark mode support
Performance optimization
Extended database functionality for persistent user data
Improved layout and feature organization








