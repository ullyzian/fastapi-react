#!/bin/bash

# Run migrations
alembic upgrade head

# Create initial data
python3 app/initial_data.py