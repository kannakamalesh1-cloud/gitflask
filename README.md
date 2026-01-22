cat > README.md << 'EOF'
# GitHub User Explorer - Flask Docker App

A simple Flask application that fetches and displays GitHub user information using the GitHub API, containerized with Docker.

## Features

- 🔍 Search any GitHub user
- 📊 View user profile information
- 📂 Display recent repositories
- 🐳 Fully containerized with Docker
- 🚀 Production-ready with Gunicorn
- 🩺 Health check endpoint

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone and navigate to the project
git clone <your-repo-url>
cd flask-github-app

# Build and run with Docker Compose
docker-compose up --build

# Access the app at http://localhost:5000
