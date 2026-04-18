# Cognitia AI App

A production-ready full-stack conversational AI web application powered by Groq's LLaMA model and MongoDB Atlas.

## Overview

Cognitia AI is a simple, single-turn question-answer application. Users enter a question, receive an instant response from the AI, and the conversation is stored in MongoDB Atlas.

### Key Features

- Single question, single response (no multi-turn conversation)
- Real-time AI response using Groq API (LLaMA 3.1 8B Instant)
- Persistent storage in MongoDB Atlas
- Clean, modern UI with loading states
- Production-ready deployment on Vercel

## Tech Stack

### Backend

- **Runtime**: Node.js 18+
- **Framework**: Express.js
- **Database**: MongoDB Atlas (Mongoose ODM)
- **AI**: Groq API (llama-3.1-8b-instant)

### Frontend

- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: CSS (custom)

## Folder Structure

```
cognitia-ai-app/
├── backend/
│   ├── config/
│   │   └── db.js           # MongoDB connection
│   ├── controllers/
│   │   └── queryController.js # Query processing logic
│   ├── models/
│   │   └── Query.js       # Mongoose schema
│   ├── routes/
│   │   └── queryRoutes.js # API routes
│   ├── server.js          # Express app entry
│   ├── vercel.json       # Vercel config
│   ├── Dockerfile        # Docker image
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main component
│   │   ├── main.jsx      # React entry
│   │   └── index.css     # Styles
│   ├── Dockerfile
│   ├── vite.config.js
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Prerequisites

- Node.js 18+
- npm or yarn
- MongoDB Atlas account
- Groq API key

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cognitia-ai-app.git
cd cognitia-ai-app
```

### 2. Backend Setup

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your credentials:

```
GROQ_API_KEY=your_groq_api_key_here
MONGO_URI=your_mongodb_atlas_connection_string_here
PORT=5000
```

Install dependencies and start:

```bash
npm install
npm start
```

### 3. Frontend Setup

```bash
cd frontend
cp .env.example .env
```

Edit `.env`:

```
VITE_API_URL=http://localhost:5000/api
```

For production, replace with your deployed backend URL:

```
VITE_API_URL=https://your-backend.vercel.app/api
```

Install dependencies and start:

```bash
npm install
npm run dev
```

### 4. Development

Open two terminals:

**Terminal 1 (Backend):**
```bash
cd backend
npm run dev
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Access the app at http://localhost:5173

## Environment Variables

### Backend (.env)

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key from [console.groq.com](https://console.groq.com) |
| `MONGO_URI` | MongoDB Atlas connection string |
| `PORT` | Server port (default: 5000) |

### Frontend (.env)

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend API URL (local or deployed) |

## MongoDB Atlas Setup

1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create database user (username/password)
4. Add IP address to whitelist (0.0.0.0 for development)
5. Get connection string from "Connect" > "Drivers"
6. Replace `<password>` with your database user password

## Groq API Usage

1. Create account at [console.groq.com](https://console.groq.com)
2. Navigate to API Keys
3. Create new API key
4. Copy key to `GROQ_API_KEY` in backend `.env`

Model used: `llama-3.1-8b-instant`

## API Documentation

### POST /api/query

Submit a question and receive an AI response.

**Request:**

```json
{
  "question": "What is the capital of France?"
}
```

**Response:**

```json
{
  "answer": "The capital of France is Paris."
}
```

**Error Response:**

```json
{
  "error": "Question is required and must be a non-empty string"
}
```

### GET /api/health

Health check endpoint.

**Response:**

```json
{
  "status": "ok"
}
```

## Deployment (Vercel)

### Backend Deployment

1. Push code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Import repository
4. Configure:
   - Framework: Other
   - Root Directory: backend
5. Add Environment Variables:
   - `GROQ_API_KEY`
   - `MONGO_URI`
6. Deploy

### Frontend Deployment

1. Go to [Vercel](https://vercel.com)
2. Import repository
3. Configure:
   - Framework: Vite
   - Root Directory: frontend
4. Add Environment Variables:
   - `VITE_API_URL=https://your-backend.vercel.app/api`
5. Deploy

## Docker Deployment

### Using docker-compose

```bash
docker-compose up --build
```

### Manual Build

**Backend:**
```bash
cd backend
docker build -t cognitia-backend .
docker run -p 5000:5000 -e GROQ_API_KEY=xxx -e MONGO_URI=xxx cognitia-backend
```

**Frontend:**
```bash
cd frontend
docker build -t cognitia-frontend .
docker run -p 5173:5173 -e VITE_API_URL=http://localhost:5000/api cognitia-frontend
```

## License

MIT

## Author

Your Name