# Use docker compose to build and run the container

FROM ubuntu:22.04
ENV PATH="/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80

# Just keep the container alive without exiting
ENTRYPOINT ["tail", "-f", "/dev/null"]
