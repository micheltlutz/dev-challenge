#!/usr/bin/env bash
# Provision the lab: dependencies, fixture database, and a sanity check that
# the harness and the reference API agree.
set -euo pipefail

echo "Installing Python dependencies..."
python -m pip install --upgrade pip --quiet
pip install -r requirements_for_dev.txt --quiet

echo "Seeding the fixture database..."
python scripts/seed.py

echo "Checking the spec layer..."
python scripts/export_openapi.py --check
python scripts/build_tokens.py --check
python scripts/validate_specs.py --quiet

cat <<'BANNER'

  dev-challenge lab is ready.

  The reference API starts automatically on port 8000.
      docs           http://localhost:8000/docs

  Demo users (password Challenge@123)
      john.doe@email.com   5 statements, balance 15491.00
      jane.roe@email.com   1 statement,  balance  4200.00

  Where to go
      specs/README.md              every challenge
      readme_files/challenged.md   how to start
      AGENTS.md                    if you are working with a coding agent

  Verify a solution
      python harness/cli.py --base-url <your-url> --challenge backend-05-balance
      python harness/cli.py --list

BANNER
