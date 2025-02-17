#!/bin/bash

GREEN='\033[1;32m'
RED='\033[1;31m'
RESET='\033[0m'

# --- Add Repository URL variable ---
REPO_URL="https://github.com/yourusername/emol.git"
# ----------------------------------

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

# --- Improved logging and error checking around git clone ---
echo -e "\nCloning repository from ${REPO_URL} to ${TEMP_DIR}..."
if ! git clone --quiet "$REPO_URL" "$TEMP_DIR"; then
    echo -e "${RED}Error cloning repository from ${REPO_URL}${RESET}"
    exit 1
fi
cd "$TEMP_DIR"
echo -e "${GREEN}Repository cloned successfully.${RESET}\n"
# ------------------------------------------------------------

if [ "$CHECK_ONLY" = true ]; then
    check_for_updates
    exit 0
fi

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

# --- Improved logging and error checking around git checkout and bootstrap ---
echo -e "Checking out version ${VERSION_TO_DEPLOY}..."
if ! git checkout "$VERSION_TO_DEPLOY"; then
    echo -e "${RED}Error checking out version ${VERSION_TO_DEPLOY}${RESET}"
    exit 1
fi
echo -e "${GREEN}Version ${VERSION_TO_DEPLOY} checked out successfully.${RESET}\n"

echo -e "Running bootstrap script for version ${VERSION_TO_DEPLOY}..."
START_TIME=$(date +%s)
if ! ./setup_files/bootstrap.sh; then
    echo -e "${RED}Deployment failed during bootstrap for version ${VERSION_TO_DEPLOY}${RESET}"
    exit 1
fi
END_TIME=$(date +%s)
DEPLOYMENT_TIME=$((END_TIME - START_TIME))
echo -e "${GREEN}Bootstrap script completed successfully in ${DEPLOYMENT_TIME} seconds.${RESET}\n"
# ---------------------------------------------------------------------------

# Tag successful deployment
DEPLOY_TAG="deploy-$VERSION_TO_DEPLOY-$(date +%Y%m%d-%H%M%S)"
git tag -a "$DEPLOY_TAG" -m "Deployed $VERSION_TO_DEPLOY"
git push origin "$DEPLOY_TAG"

echo -e "${GREEN}Successfully deployed version $VERSION_TO_DEPLOY${RESET}"
echo -e "${GREEN}Deployment tag pushed: ${DEPLOY_TAG}${RESET}" 