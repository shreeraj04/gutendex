#!/bin/bash

# Load environment variables
source .env

# Create the database
createdb gutenberg

# Restore the database from the dump file
pg_restore -d gutenberg dump_file.dump

echo "Database initialized successfully!"