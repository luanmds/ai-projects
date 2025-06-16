#!/bin/bash

# Run script for Notion MCP Server
# This script starts the MCP server for use with MCP clients

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}" >&2
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}" >&2
}

print_error() {
    echo -e "${RED}❌ $1${NC}" >&2
}

print_info "Starting Notion MCP Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found!"
    print_info "Please run: bash setup.sh"
    exit 1
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    print_info "Please run: bash setup.sh"
    exit 1
fi

# Check if NOTION_API_KEY is configured
source .env
if [ -z "$NOTION_API_KEY" ] || [ "$NOTION_API_KEY" = "your_notion_api_key_here" ]; then
    print_error "NOTION_API_KEY not configured!"
    print_info "Please edit .env file and set your Notion API key"
    print_info "Get your API key from: https://www.notion.so/my-integrations"
    exit 1
fi

# Check if all dependencies are installed
print_info "Checking dependencies..."
python -c "import mcp; import notion_client; import pydantic_settings" 2>/dev/null || {
    print_warning "Dependencies missing, installing..."
    pip install -r requirements.txt --quiet
    if [ $? -ne 0 ]; then
        print_error "Failed to install dependencies"
        exit 1
    fi
    print_success "Dependencies installed"
}

print_success "Dependencies OK"

# Start the MCP server
print_info "Starting MCP server..."
print_info "Server communicates via stdio (JSON-RPC)"
print_info "Ready for MCP client connections..."

# Run the server - all output to stderr except the actual MCP communication
exec python -m src.main