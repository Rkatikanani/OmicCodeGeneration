# OmicCodeGeneration

A web application that generates omic analysis code from natural language using a model context protocol.

## Project Structure

```
omic-code-generation/
├── frontend/           # React + TypeScript frontend
├── backend/           # FastAPI Python backend
└── docs/             # Project documentation
```

## Features

- Natural language to omic analysis code generation
- Model context protocol implementation
- Interactive web interface
- Real-time code generation
- Support for various omic analysis types

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Run the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

## Development

- Backend API runs on: http://localhost:8000
- Frontend development server runs on: http://localhost:3000

## License

MIT