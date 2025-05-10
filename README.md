# CareBuddy - AI-Powered Healthcare Assistant

CareBuddy is an innovative healthcare platform that leverages artificial intelligence to provide personalized medical assistance and support. The platform connects patients with healthcare professionals and offers intelligent health monitoring and guidance.

## Features

- 🤖 AI-powered health monitoring and assistance
- 👨‍⚕️ Doctor-patient matching system
- 📱 User-friendly interface for both patients and healthcare providers
- 🔒 Secure and private health data management
- 💬 Real-time communication between patients and doctors

## Tech Stack

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Shadcn UI Components

### Backend
- Python
- FastAPI
- SQLite
- RAG (Retrieval-Augmented Generation) for AI responses

## Getting Started

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Aditya-raj22/CareBuddy.git
cd CareBuddy
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend/cb_v1
npm install
```

4. Create a `.env` file in the backend directory with your configuration:
```env
DATABASE_URL=sqlite:///./carebuddy.db
SECRET_KEY=your-secret-key
```

### Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend/cb_v1
npm run dev
```

The application will be available at `http://localhost:3000`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any queries or support, please reach out to [your-email@example.com]
