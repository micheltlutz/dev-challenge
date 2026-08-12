# Portable verification harness.
#
# Build from the repository root so the spec layer can be copied in:
#   docker build -f harness/Dockerfile -t dev-challenge-harness .
#
# Run against your own project:
#   docker run --rm --network host dev-challenge-harness \
#     --base-url http://localhost:3000 --challenge backend-05-balance

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEV_CHALLENGE_SPECS=/harness/specs

WORKDIR /harness

RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir "pytest>=8" "httpx>=0.27"

# The scorecard quotes the acceptance criteria, so the specs travel with it.
COPY specs /harness/specs
COPY harness /harness

ENTRYPOINT ["python", "/harness/cli.py"]
CMD ["--help"]
