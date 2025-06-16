#!/bin/bash

# Setup script for Notion MCP Server

echo "🚀 Setting up Notion MCP Server..."
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: You need to configure your Notion API key!"
    echo "   1. Go to https://www.notion.so/my-integrations"
    echo "   2. Create a new integration"
    echo "   3. Copy the 'Internal Integration Token'"
    echo "   4. Edit the .env file and set NOTION_API_KEY=your_token_here"
    echo ""
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the environment: source venv/bin/activate"
echo "2. Configure your Notion API key in .env file"
echo "3. Share your Notion pages with the integration"
echo "4. Test the setup: python test_notion.py"
echo "5. Run the MCP server: python -m src.main"
echo ""
echo "📖 See README.md for detailed usage instructions"
