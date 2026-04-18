# Vibecoded - Project Generation Context

This project was generated using AI-assisted development tools.

## Tools Used

- **OpenCode** - Primary development environment (https://opencode.ai)
- **ChatGPT** - Code review and assistance

## Prompt/Requirements Used

The user provided a comprehensive specification for building a full-stack conversational AI web app with the following requirements:

1. **Architecture**: Monorepo with /frontend (React + Vite) and /backend (Node.js + Express)
2. **Core Functionality**: Single question → Groq API (llama-3.1-8b-instant) → Single response
3. **Storage**: MongoDB Atlas for storing question/response pairs
4. **API**: POST /api/query endpoint
5. **Security**: Environment variables (.env) for API keys and database URI
6. **UI**: Simple input box, submit button, response display
7. **Deployment**: Vercel for both frontend and backend
8. **Documentation**: README.md and vibecoded.md

## Configuration Details

### Backend Structure

- `server.js` - Main entry point with Express setup
- `routes/queryRoutes.js` - API route definitions
- `controllers/queryController.js` - Business logic for Groq API and MongoDB
- `models/Query.js` - Mongoose schema for question/answer storage
- `config/db.js` - MongoDB connection
- `vercel.json` - Vercel serverless deployment config

### Frontend Structure

- `src/App.jsx` - Main React component with form and response display
- `src/main.jsx` - React entry point
- `src/index.css` - Styled UI components
- `vite.config.js` - Vite configuration
- `.env.example` - Environment variable template

### Deployment

- **Backend**: Vercel serverless API routes
- **Frontend**: Vercel static deployment
- **Docker**: Dockerfiles and docker-compose.yml for local development

## Implementation Notes

- Single-turn only (no chat history, no memory, no authentication)
- Input validation for question length and format
- Proper error handling with try/catch
- Loading state during API calls
- Uses fetch API for Groq integration
- Clean, modular code following Express/React best practices