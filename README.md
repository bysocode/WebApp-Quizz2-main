# WebApp-Quizz2

A full-stack web application for creating and taking quizzes online. This project consists of a Python Flask backend API and a Vue 3 frontend built with Vite.

## Project Overview

WebApp-Quizz2 is a comprehensive quiz platform that allows users to:
- Take interactive quizzes
- View quiz information and available questions
- Track quiz scores
- Manage quiz questions and answers (admin features)
- Secure access with JWT authentication

The application is built with a modern tech stack:
- **Backend**: Flask (Python) with SQLite database
- **Frontend**: Vue 3 with Vite, Bootstrap 5 for styling
- **API**: RESTful API with JWT authentication
- **Database**: SQLite for persistent data storage

## Project Structure

```
WebApp-Quizz2/
├── quiz-app/
│   ├── quiz-api/          # Flask backend API (Python)
│   │   ├── app.py         # Main Flask application
│   │   ├── model.py       # Data models
│   │   ├── database.py    # Database operations
│   │   ├── requirements.txt
│   │   └── ...
│   │
│   ├── quiz-ui/           # Vue 3 frontend (JavaScript)
│   │   ├── src/           # Vue components and application logic
│   │   ├── public/        # Static assets
│   │   ├── package.json
│   │   └── vite.config.js
│   │
│   └── QuizDB.db          # SQLite database (generated)
│
└── README.md              # This file
```

## Getting Started

### Prerequisites

- **Node.js** 16.x or higher (for frontend)
- **Python** 3.8 or higher (for backend)
- **npm** or **yarn** (Node package manager)
- **pip** (Python package manager)

### Installation & Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd WebApp-Quizz2
```

#### 2. Backend Setup (Flask API)

Navigate to the quiz-api directory:

```bash
cd quiz-app/quiz-api
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database (optional - will be created on first run):

```bash
python rebuild_db.py
```

#### 3. Frontend Setup (Vue 3)

Navigate to the quiz-ui directory:

```bash
cd ../quiz-ui
```

Install Node dependencies:

```bash
npm install
```

## Running the Application

### Start the Backend Server

From the `quiz-app/quiz-api` directory:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

**Alternatively, using Gunicorn (production):**

```bash
gunicorn -w 4 app:app
```

### Start the Frontend Development Server

From the `quiz-app/quiz-ui` directory:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` (or the port shown in terminal)

### Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

## Backend (Flask API) - Available Endpoints

The Flask API provides the following main endpoints:

- `GET /` - Hello endpoint
- `POST /login` - User login with password
- `GET /quiz-info` - Get quiz information (total questions, scores)
- `GET /questions/<id>` - Get question by ID
- `POST /questions` - Create new question (admin)
- `PUT /questions/<id>` - Update question (admin)
- `DELETE /questions/<id>` - Delete question (admin)
- `POST /rebuild-db` - Rebuild database (admin)

**Authentication**: The API uses JWT tokens for secure access.

## Frontend (Vue 3 + Vite)

### Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint files with ESLint
npm run lint

# Format code with Prettier
npm run format
```

### Features

- Interactive quiz interface
- Real-time score calculation
- Responsive design with Bootstrap 5
- Vue Router for navigation
- Axios for API communication

## Authentication

The application uses JWT (JSON Web Tokens) for authentication:

1. Users login with a password
2. Server returns a JWT token
3. Token is stored in the client and included in subsequent API requests
4. Server validates token before processing requests

Default password hash is configured in `app.py`.

## Database

The application uses SQLite for data persistence:

- **Database File**: `QuizDB.db`
- **Tables**: Users, Questions, Answers, Participations, Scores
- **Connection**: Configured in `database.py`

To reset the database:

```bash
python rebuild_db.py
# or via API
curl -X POST http://localhost:5000/rebuild-db
```

## Development

### Code Style

Frontend code is formatted using Prettier and linted with ESLint:

```bash
# Format Vue files
npm run format

# Lint with auto-fix
npm run lint
```

### IDE Setup

Recommended IDE: **VSCode** with these extensions:
- Volar (Vue language support)
- ESLint
- Prettier
- Python extension

## Configuration

### Frontend Configuration

- **Vite Config**: `quiz-app/quiz-ui/vite.config.js`
- **ESLint Config**: `quiz-app/quiz-ui/eslint.config.js`
- **Prettier Config**: `quiz-app/quiz-ui/.prettierrc.json`
- **Environment Variables**: `quiz-app/quiz-ui/.env.development`

### Backend Configuration

- Flask app configuration is in `quiz-app/quiz-api/app.py`
- Database configuration is in `quiz-app/quiz-api/database.py`

## Docker Support

The project includes Docker support:

```bash
cd quiz-app/quiz-api
docker build -t quiz-api .
docker run -p 5000:5000 quiz-api
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Follow the code style guidelines
4. Test your changes
5. Submit a pull request

## License

This project is licensed under the ISC License - see the LICENSE file for details.

## Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify port 5000 is not in use

### Frontend won't start
- Ensure Node 16+ is installed
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Check that port 5173 is not in use

### Database issues
- Delete `QuizDB.db` and run `python rebuild_db.py` to reset
- Check database permissions

### CORS errors
- Ensure the backend Flask-CORS is properly configured
- Check that frontend is making requests to the correct API URL

## Contact & Support

For issues, questions, or suggestions, please open an issue on the repository or contact me @ philemyjulienaymar@gmail.com