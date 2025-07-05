#!/bin/bash

# Tech Trades Deployment Script
# This script helps prepare and deploy the application to Vercel

echo "🚀 Tech Trades Deployment Script"
echo "================================"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    print_error "vercel.json not found. Please run this script from the project root."
    exit 1
fi

print_status "Found vercel.json configuration"

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    print_error "Frontend directory not found"
    exit 1
fi

print_status "Frontend directory found"

# Check if api directory exists
if [ ! -d "api" ]; then
    print_error "API directory not found"
    exit 1
fi

print_status "API directory found"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js first."
    exit 1
fi

print_status "Node.js is available"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_status "npm is available"

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    print_error "Python is not installed. Please install Python first."
    exit 1
fi

print_status "Python is available"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found"
    exit 1
fi

print_status "requirements.txt found"

# Check if frontend package.json exists
if [ ! -f "frontend/package.json" ]; then
    print_error "frontend/package.json not found"
    exit 1
fi

print_status "frontend/package.json found"

# Check if companies.json exists in api directory
if [ ! -f "api/companies.json" ]; then
    print_error "api/companies.json not found"
    exit 1
fi

print_status "api/companies.json found"

echo ""
echo "🔧 Installing dependencies..."

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
if npm install; then
    print_status "Frontend dependencies installed successfully"
else
    print_error "Failed to install frontend dependencies"
    exit 1
fi

echo ""
echo "🏗️ Building frontend..."

# Build frontend
if npm run build; then
    print_status "Frontend build completed successfully"
else
    print_error "Frontend build failed"
    exit 1
fi

# Go back to root directory
cd ..

echo ""
echo "🧪 Running pre-deployment checks..."

# Check if build output exists
if [ ! -d "frontend/dist" ]; then
    print_error "Frontend dist directory not found after build"
    exit 1
fi

print_status "Frontend build output found"

# Check if index.html exists in dist
if [ ! -f "frontend/dist/index.html" ]; then
    print_error "index.html not found in dist directory"
    exit 1
fi

print_status "index.html found in dist directory"

# Check if API index.py exists
if [ ! -f "api/index.py" ]; then
    print_error "api/index.py not found"
    exit 1
fi

print_status "API index.py found"

echo ""
echo "✅ Pre-deployment checks passed!"
echo ""

# Check if Vercel CLI is installed
if command -v vercel &> /dev/null; then
    print_status "Vercel CLI is available"
    echo ""
    echo "🚀 Ready to deploy!"
    echo ""
    echo "Choose your deployment method:"
    echo "1. Deploy now with Vercel CLI"
    echo "2. Get manual deployment instructions"
    echo ""
    read -p "Enter your choice (1 or 2): " choice
    
    case $choice in
        1)
            echo ""
            echo "🚀 Starting deployment..."
            if vercel; then
                print_status "Deployment completed successfully!"
                echo ""
                echo "Your application should now be live on Vercel!"
            else
                print_error "Deployment failed. Please check the error messages above."
            fi
            ;;
        2)
            echo ""
            echo "📋 Manual Deployment Instructions:"
            echo "================================="
            echo "1. Go to https://vercel.com/dashboard"
            echo "2. Click 'New Project'"
            echo "3. Import your Git repository"
            echo "4. Configure the project:"
            echo "   - Framework Preset: Other"
            echo "   - Build Command: cd frontend && npm run build"
            echo "   - Output Directory: frontend/dist"
            echo "   - Install Command: cd frontend && npm install"
            echo "5. Click 'Deploy'"
            echo ""
            echo "For more detailed instructions, see DEPLOYMENT.md"
            ;;
        *)
            echo "Invalid choice. Please run the script again."
            ;;
    esac
else
    print_warning "Vercel CLI is not installed"
    echo ""
    echo "📋 Manual Deployment Instructions:"
    echo "================================="
    echo "1. Install Vercel CLI: npm i -g vercel"
    echo "2. Login to Vercel: vercel login"
    echo "3. Deploy: vercel"
    echo ""
    echo "Or deploy via Vercel Dashboard:"
    echo "1. Go to https://vercel.com/dashboard"
    echo "2. Click 'New Project'"
    echo "3. Import your Git repository"
    echo "4. Configure the project:"
    echo "   - Framework Preset: Other"
    echo "   - Build Command: cd frontend && npm run build"
    echo "   - Output Directory: frontend/dist"
    echo "   - Install Command: cd frontend && npm install"
    echo "5. Click 'Deploy'"
    echo ""
    echo "For more detailed instructions, see DEPLOYMENT.md"
fi

echo ""
echo "🎉 Deployment preparation complete!"
echo "For troubleshooting, check DEPLOYMENT.md" 