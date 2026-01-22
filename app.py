cat > app.py << 'EOF'
from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# GitHub API configuration
GITHUB_API_URL = "https://api.github.com"
DEFAULT_USER = "torvalds"  # Linus Torvalds as default

@app.route('/')
def index():
    """Main page with GitHub user search"""
    return render_template('index.html')

@app.route('/api/user/<username>')
def get_user_info(username):
    """Fetch GitHub user information"""
    try:
        response = requests.get(f"{GITHUB_API_URL}/users/{username}")
        if response.status_code == 200:
            user_data = response.json()
            
            # Format the data
            formatted_data = {
                'username': user_data['login'],
                'name': user_data.get('name', 'N/A'),
                'avatar_url': user_data['avatar_url'],
                'bio': user_data.get('bio', 'No bio available'),
                'public_repos': user_data['public_repos'],
                'followers': user_data['followers'],
                'following': user_data['following'],
                'created_at': datetime.strptime(user_data['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%B %d, %Y'),
                'html_url': user_data['html_url'],
                'blog': user_data.get('blog', 'N/A'),
                'location': user_data.get('location', 'N/A')
            }
            return jsonify(formatted_data)
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/repos/<username>')
def get_user_repos(username):
    """Fetch user's repositories"""
    try:
        response = requests.get(f"{GITHUB_API_URL}/users/{username}/repos?sort=updated&per_page=10")
        if response.status_code == 200:
            repos = response.json()
            formatted_repos = []
            
            for repo in repos[:10]:  # Limit to 10 repos
                formatted_repos.append({
                    'name': repo['name'],
                    'description': repo.get('description', 'No description'),
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'language': repo.get('language', 'N/A'),
                    'updated_at': datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'),
                    'html_url': repo['html_url']
                })
            return jsonify(formatted_repos)
        else:
            return jsonify({'error': 'Unable to fetch repositories'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Docker monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'container_id': os.uname().nodename if hasattr(os, 'uname') else 'unknown'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF
