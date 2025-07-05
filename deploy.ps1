# Tech Trades Deployment Script (PowerShell)
# This script helps prepare and deploy the application to Vercel

Write-Host "🚀 Tech Trades Deployment Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Function to print colored output
function Print-Status {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Print-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Print-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

# Check if we're in the right directory
if (-not (Test-Path "vercel.json")) {
    Print-Error "vercel.json not found. Please run this script from the project root."
    exit 1
}

Print-Status "Found vercel.json configuration"

# Check if frontend directory exists
if (-not (Test-Path "frontend")) {
    Print-Error "Frontend directory not found"
    exit 1
}

Print-Status "Frontend directory found"

# Check if api directory exists
if (-not (Test-Path "api")) {
    Print-Error "API directory not found"
    exit 1
}

Print-Status "API directory found"

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Print-Status "Node.js is available ($nodeVersion)"
} catch {
    Print-Error "Node.js is not installed. Please install Node.js first."
    exit 1
}

# Check if npm is installed
try {
    $npmVersion = npm --version
    Print-Status "npm is available ($npmVersion)"
} catch {
    Print-Error "npm is not installed. Please install npm first."
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = python --version
    Print-Status "Python is available ($pythonVersion)"
} catch {
    try {
        $pythonVersion = python3 --version
        Print-Status "Python is available ($pythonVersion)"
    } catch {
        Print-Error "Python is not installed. Please install Python first."
        exit 1
    }
}

# Check if requirements.txt exists
if (-not (Test-Path "requirements.txt")) {
    Print-Error "requirements.txt not found"
    exit 1
}

Print-Status "requirements.txt found"

# Check if frontend package.json exists
if (-not (Test-Path "frontend/package.json")) {
    Print-Error "frontend/package.json not found"
    exit 1
}

Print-Status "frontend/package.json found"

# Check if companies.json exists in api directory
if (-not (Test-Path "api/companies.json")) {
    Print-Error "api/companies.json not found"
    exit 1
}

Print-Status "api/companies.json found"

Write-Host ""
Write-Host "🔧 Installing dependencies..." -ForegroundColor Cyan

# Install frontend dependencies
Write-Host "Installing frontend dependencies..."
Set-Location frontend
try {
    npm install
    Print-Status "Frontend dependencies installed successfully"
} catch {
    Print-Error "Failed to install frontend dependencies"
    exit 1
}

Write-Host ""
Write-Host "🏗️ Building frontend..." -ForegroundColor Cyan

# Build frontend
try {
    npm run build
    Print-Status "Frontend build completed successfully"
} catch {
    Print-Error "Frontend build failed"
    exit 1
}

# Go back to root directory
Set-Location ..

Write-Host ""
Write-Host "🧪 Running pre-deployment checks..." -ForegroundColor Cyan

# Check if build output exists
if (-not (Test-Path "frontend/dist")) {
    Print-Error "Frontend dist directory not found after build"
    exit 1
}

Print-Status "Frontend build output found"

# Check if index.html exists in dist
if (-not (Test-Path "frontend/dist/index.html")) {
    Print-Error "index.html not found in dist directory"
    exit 1
}

Print-Status "index.html found in dist directory"

# Check if API index.py exists
if (-not (Test-Path "api/index.py")) {
    Print-Error "api/index.py not found"
    exit 1
}

Print-Status "API index.py found"

Write-Host ""
Write-Host "✅ Pre-deployment checks passed!" -ForegroundColor Green
Write-Host ""

# Check if Vercel CLI is installed
try {
    $vercelVersion = vercel --version
    Print-Status "Vercel CLI is available ($vercelVersion)"
    Write-Host ""
    Write-Host "🚀 Ready to deploy!" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Choose your deployment method:"
    Write-Host "1. Deploy now with Vercel CLI"
    Write-Host "2. Get manual deployment instructions"
    Write-Host ""
    $choice = Read-Host "Enter your choice (1 or 2)"
    
    switch ($choice) {
        "1" {
            Write-Host ""
            Write-Host "🚀 Starting deployment..." -ForegroundColor Cyan
            try {
                vercel
                Print-Status "Deployment completed successfully!"
                Write-Host ""
                Write-Host "Your application should now be live on Vercel!" -ForegroundColor Green
            } catch {
                Print-Error "Deployment failed. Please check the error messages above."
            }
        }
        "2" {
            Write-Host ""
            Write-Host "📋 Manual Deployment Instructions:" -ForegroundColor Cyan
            Write-Host "================================="
            Write-Host "1. Go to https://vercel.com/dashboard"
            Write-Host "2. Click 'New Project'"
            Write-Host "3. Import your Git repository"
            Write-Host "4. Configure the project:"
            Write-Host "   - Framework Preset: Other"
            Write-Host "   - Build Command: cd frontend && npm run build"
            Write-Host "   - Output Directory: frontend/dist"
            Write-Host "   - Install Command: cd frontend && npm install"
            Write-Host "5. Click 'Deploy'"
            Write-Host ""
            Write-Host "For more detailed instructions, see DEPLOYMENT.md"
        }
        default {
            Write-Host "Invalid choice. Please run the script again." -ForegroundColor Yellow
        }
    }
} catch {
    Print-Warning "Vercel CLI is not installed"
    Write-Host ""
    Write-Host "📋 Manual Deployment Instructions:" -ForegroundColor Cyan
    Write-Host "================================="
    Write-Host "1. Install Vercel CLI: npm i -g vercel"
    Write-Host "2. Login to Vercel: vercel login"
    Write-Host "3. Deploy: vercel"
    Write-Host ""
    Write-Host "Or deploy via Vercel Dashboard:"
    Write-Host "1. Go to https://vercel.com/dashboard"
    Write-Host "2. Click 'New Project'"
    Write-Host "3. Import your Git repository"
    Write-Host "4. Configure the project:"
    Write-Host "   - Framework Preset: Other"
    Write-Host "   - Build Command: cd frontend && npm run build"
    Write-Host "   - Output Directory: frontend/dist"
    Write-Host "   - Install Command: cd frontend && npm install"
    Write-Host "5. Click 'Deploy'"
    Write-Host ""
    Write-Host "For more detailed instructions, see DEPLOYMENT.md"
}

Write-Host ""
Write-Host "🎉 Deployment preparation complete!" -ForegroundColor Green
Write-Host "For troubleshooting, check DEPLOYMENT.md" 