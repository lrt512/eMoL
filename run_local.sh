#! /bin/bash

case "$1" in
  up)
    docker compose up --build -d
    ;;
  down)
    docker compose down
    ;;
  shell)
    docker exec -it emol-app-1 /bin/bash
    ;;
  manage)
    shift  # Remove 'manage' from the arguments
    docker exec -it emol-app-1 poetry run python manage.py "$@"
    ;;
  *)
    echo "Usage: $0 {up|down|shell|manage}"
    echo
    echo "Commands:"
    echo "  up      Start the development environment"
    echo "  down    Stop the development environment"
    echo "  shell   Open a shell in the app container"
    echo "  manage  Run Django management commands, e.g.:"
    echo "          $0 manage create_test_user admin@emol.ca --superuser"
    exit 1
    ;;
esac
