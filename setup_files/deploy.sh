#!/bin/bash

GREEN='\033[1;32m'
RED='\033[1;31m'
RESET='\033[0m'

# --- Add Repository URL variable ---
REPO_URL="https://github.com/yourusername/emol.git"
BACKUP_DIR="/opt/emol_backup"
# ----------------------------------

MAINTENANCE_PAGE="/opt/emol/maintenance.html"
DEPLOY_LOG="/var/log/emol/deployments.log"

show_help() {
    cat << EOF
EMOL Deployment Script

Usage: $0 [options]

Options:
    --check         Only check if updates are available
    --dry-run      Show what would be deployed
    --force        Deploy specific version (e.g., --force v0.1.0)
    --help         Show this help message

Example:
    $0              # Check and deploy latest version if needed
    $0 --check     # Only check for updates
    $0 --dry-run   # Show what would be deployed
    $0 --force v0.1.0  # Force deploy specific version
EOF
    exit 0
}

get_current_version() {
    if [ -f "/opt/emol/VERSION" ]; then
        cat "/opt/emol/VERSION"
    else
        echo "0.0.0"
    fi
}

get_latest_version() {
    # Get the latest version tag from git
    git fetch --tags
    git tag -l "v*" | sort -V | tail -n1
}

check_for_updates() {
    CURRENT_VERSION="v$(get_current_version)"
    LATEST_VERSION=$(get_latest_version)
    
    echo "Current version: $CURRENT_VERSION"
    echo "Latest version:  $LATEST_VERSION"
    
    if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
        echo -e "${GREEN}System is up to date${RESET}"
        return 1
    else
        echo -e "${GREEN}Update available: $LATEST_VERSION${RESET}"
        return 0
    fi
}

pre_deploy_checks() {
    echo "Running pre-deployment checks..."
    
    # Check disk space
    FREE_SPACE=$(df -m /opt | awk 'NR==2 {print $4}')
    if [ "$FREE_SPACE" -lt 2048 ]; then # 2GB minimum
        echo -e "${RED}Insufficient disk space for deployment${RESET}"
        exit 1
    }

    # Check current application status
    if ! /etc/init.d/emol status > /dev/null; then
        echo -e "${RED}Warning: Application is not running${RESET}"
        read -p "Continue deployment? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    }
}

backup_current() {
    echo "Creating backup..."
    BACKUP_NAME="emol_backup_$(date +%Y%m%d_%H%M%S)"
    BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"
    
    mkdir -p "$BACKUP_DIR"
    # Keep only last 5 backups
    ls -t "$BACKUP_DIR" | tail -n +6 | xargs -I {} rm -rf "$BACKUP_DIR/{}"
    
    if ! cp -r /opt/emol "$BACKUP_PATH"; then
        echo -e "${RED}Backup failed${RESET}"
        exit 1
    fi
    echo -e "${GREEN}Backup created at $BACKUP_PATH${RESET}"
}

rollback() {
    echo -e "${RED}Deployment failed - rolling back...${RESET}"
    if [ -d "$BACKUP_PATH" ]; then
        rm -rf /opt/emol
        cp -r "$BACKUP_PATH" /opt/emol
        /etc/init.d/emol restart
        service nginx restart
        echo -e "${GREEN}Rollback complete${RESET}"
    else
        echo -e "${RED}No backup found for rollback${RESET}"
    fi
}

enable_maintenance() {
    # Simple maintenance page
    cat > "$MAINTENANCE_PAGE" << 'EOF'
<!DOCTYPE html>
<html>
<body>
    <h1>eMoL System Maintenance</h1>
    <p>The system is currently being updated. Please check back in 5 minutes.</p>
</body>
</html>
EOF

    # Update nginx to serve maintenance page
    sed -i 's|proxy_pass http://unix:${SOCKET_PATH};|return 503;|' /etc/nginx/sites-enabled/emol.conf
    sed -i '/return 503;/a\        error_page 503 /maintenance.html;\n        location = /maintenance.html {\n            root /opt/emol;\n        }' /etc/nginx/sites-enabled/emol.conf
    
    service nginx reload
}

disable_maintenance() {
    # Restore normal nginx config
    sed -i 's|return 503;|proxy_pass http://unix:${SOCKET_PATH};|' /etc/nginx/sites-enabled/emol.conf
    sed -i '/error_page 503/,+4d' /etc/nginx/sites-enabled/emol.conf
    rm -f "$MAINTENANCE_PAGE"
    
    service nginx reload
}

log_deployment() {
    local status=$1
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $VERSION_TO_DEPLOY - $status" >> "$DEPLOY_LOG"
}

deploy() {
    echo "Starting deployment..."
    log_deployment "started"
    
    enable_maintenance
    # Graceful stop
    /etc/init.d/emol stop
    
    # Deploy new version
    if ! ./setup_files/bootstrap.sh; then
        rollback
        disable_maintenance
        log_deployment "failed - rolled back"
        exit 1
    fi
    
    # Restart services
    if ! /etc/init.d/emol start || ! service nginx restart; then
        rollback
        disable_maintenance
        log_deployment "failed - rolled back"
        exit 1
    fi
    
    disable_maintenance
    log_deployment "completed"
}

# Parse arguments
DRY_RUN=false
CHECK_ONLY=false
FORCE_VERSION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --check)
            CHECK_ONLY=true
            shift
            ;;
        --force)
            shift
            FORCE_VERSION=$1
            shift
            ;;
        --help)
            show_help
            ;;
        *)
            echo -e "${RED}Unknown argument: $1${RESET}"
            show_help
            ;;
    esac
done

# Create temp directory for git operations
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo -e "\nCloning repository from ${REPO_URL} to ${TEMP_DIR}..."
if ! git clone --quiet "$REPO_URL" "$TEMP_DIR"; then
    echo -e "${RED}Error cloning repository from ${REPO_URL}${RESET}"
    exit 1
fi
cd "$TEMP_DIR"

if [ "$CHECK_ONLY" = true ]; then
    check_for_updates
    exit 0
fi

# Run pre-deployment checks
pre_deploy_checks

# Create backup
backup_current

if [ -n "$FORCE_VERSION" ]; then
    VERSION_TO_DEPLOY=$FORCE_VERSION
else
    check_for_updates
    if [ $? -eq 1 ] && [ "$DRY_RUN" = false ]; then
        exit 0
    fi
    VERSION_TO_DEPLOY=$(get_latest_version)
fi

if [ "$DRY_RUN" = true ]; then
    echo -e "Would deploy version $VERSION_TO_DEPLOY"
    ./setup_files/bootstrap.sh --dry-run
    exit 0
fi

# Perform deployment
deploy

# Tag successful deployment
DEPLOY_TAG="deploy-$VERSION_TO_DEPLOY-$(date +%Y%m%d-%H%M%S)"
git tag -a "$DEPLOY_TAG" -m "Deployed $VERSION_TO_DEPLOY"
git push origin "$DEPLOY_TAG"

echo -e "${GREEN}Successfully deployed version $VERSION_TO_DEPLOY${RESET}"
echo -e "${GREEN}Deployment tag pushed: ${DEPLOY_TAG}${RESET}" 