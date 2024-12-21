# eMoL (electronic Ministry of Lists)

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Git

### Quick Start
1. Clone the repository:
```bash
git clone <repository-url>
cd emol
```

2. Start the development environment:
```bash
./run_local.sh up
```

3. Access the application at http://localhost:8000

### Development Environment

The development environment includes:
- Django application server
- MySQL database
- LocalStack (for AWS SSM Parameter Store emulation)
- Mock OAuth server for authentication

#### Development Tools

The `run_local.sh` script provides several commands:
```bash
./run_local.sh up      # Start the development environment
./run_local.sh down    # Stop the development environment
./run_local.sh shell   # Open a shell in the app container
./run_local.sh manage  # Run Django management commands
```

#### Authentication

Development uses a mock OAuth server that accepts any registered user:
1. Log in with that user's email (password can be anything)
2. The mock server provides OAuth tokens just like Google would

#### Database

The development database:
- Runs in a Docker container
- Uses MySQL
- Persists data between restarts in a Docker volume
- Automatically configured with test credentials

## Production Setup

### Google OAuth Configuration
1. Go to the Google Developers Console (https://console.developers.google.com/)
2. Create a new project or select an existing project
3. Enable the Google OAuth2 API
4. Create OAuth credentials:
   - Application type: Web application
   - Add authorized redirect URIs:
     - https://your-domain.com/auth/callback
     - https://your-domain.com/auth/admin/oauth/

### AWS Configuration
Store the following parameters in SSM Parameter Store:
- `/emol/django_settings_module`
- `/emol/oauth_client_id` (from Google OAuth setup)
- `/emol/oauth_client_secret` (from Google OAuth setup)
- `/emol/db_host`
- `/emol/db_name`
- `/emol/db_user`
- `/emol/db_password`

### Database Setup
1. Create a MySQL database
2. Create database user with appropriate permissions
3. Update SSM parameters with database credentials

### Application Deployment
1. Clone the repository
2. Run the installation script:
```bash
cd setup_files
chmod +x *.sh
./setup.sh
```

3. Configure nginx (if needed)
4. Start the application service

## Contributing

Please see CONTRIBUTING.md for development guidelines and coding standards.