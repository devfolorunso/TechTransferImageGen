# Tech Transfer Announcement

A modern web application that allows tech professionals to create professional flyers announcing their career moves between companies. Built with Python Flask backend and React frontend.

## Features

- **Modern UI**: Clean, responsive design with glassmorphism effects
- **Professional Flyers**: Generate high-quality announcement flyers with company logos
- **Company Database**: Pre-populated with 80+ major tech companies
- **Custom Companies**: Add any company not in the predefined list
- **Logo Integration**: Automatic company logo fetching using Clearbit Logo API
- **Smart Selectors**: Searchable company dropdowns with logo previews
- **Custom Typography**: Spicy Rice font integration for eye-catching names
- **Image Generation**: Automated flyer creation using Python PIL
- **File Upload**: Support for profile picture uploads
- **Instant Download**: Download generated flyers as PNG files
- **Real-time Preview**: See live preview with logos as you fill out the form

## Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **PIL (Pillow)** - Image processing and generation
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling framework
- **Lucide React** - Icon library
- **Axios** - HTTP client

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Flask server**:
   ```bash
   cd backend
   python app.py
   ```

   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

1. **Open the application** in your browser at `http://localhost:3000`

2. **Fill out the form** with your information:
   - Full Name
   - Former Company (dropdown)
   - New Company (dropdown)
   - Role/Position
   - Profile picture (upload)

3. **Generate your flyer** by clicking "Generate Flyer"

4. **Download your flyer** once it's generated

### Adding Custom Companies

If your company isn't in the predefined list:

1. **Click the company dropdown** (Former or New Company)
2. **Scroll to the bottom** of the dropdown list
3. **Click "Add Custom Company"** (marked with a blue + icon)
4. **Enter your company name** in the input field
5. **Click "Add Company"** or press Enter

The application will automatically attempt to find a logo for your custom company using common domain patterns. If no logo is found, the flyer will display the company name without a logo.

## Project Structure

```
TechTransferAnnouncement/
├── backend/
│   ├── app.py              # Flask application
│   ├── companies.json      # Tech companies database
│   ├── fonts/              # Downloaded custom fonts (auto-created)
│   ├── uploads/            # Temporary file uploads
│   └── generated/          # Generated flyer images
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── CompanySelector.jsx # Custom company selector component
│   │   ├── main.jsx       # React entry point
│   │   └── index.css      # Tailwind CSS styles
│   ├── public/
│   ├── index.html         # HTML template
│   ├── package.json       # Node.js dependencies
│   ├── vite.config.js     # Vite configuration
│   └── tailwind.config.js # Tailwind configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## API Endpoints

### GET /api/companies
Returns a list of available tech companies with logo URLs for the dropdowns.

**Response:**
```json
{
  "companies": [
    {
      "name": "Google",
      "domain": "google.com",
      "logo": "https://logo.clearbit.com/google.com"
    },
    {
      "name": "Apple", 
      "domain": "apple.com",
      "logo": "https://logo.clearbit.com/apple.com"
    },
    ...
  ]
}
```

### POST /api/generate-flyer
Generates a tech transfer announcement flyer.

**Request:** FormData with:
- `name` (string): Full name
- `former_company` (string): Former company name
- `new_company` (string): New company name
- `role` (string): Job role/position
- `date` (string): Date of transition
- `profile_image` (file): Profile picture

**Response:**
```json
{
  "success": true,
  "image_data": "base64_encoded_image_data",
  "filename": "generated_filename.png"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000000"
}
```

## Customization

### Adding More Companies
Edit the `backend/companies.json` file to add more companies:

```json
{
  "companies": [
    {"name": "Google", "domain": "google.com"},
    {"name": "Apple", "domain": "apple.com"},
    {"name": "YourCompany", "domain": "yourcompany.com"},
    {"name": "AnotherCompany", "domain": "anothercompany.com"}
  ]
}
```

The application automatically loads companies from this JSON file at startup. If the file is missing or corrupted, it will fall back to a basic set of companies.

### Logo Integration
The application uses the Clearbit Logo API to automatically fetch company logos:
- **Free**: No API key required
- **High Quality**: Vector-based logos when available
- **Automatic**: Logos are fetched based on company domains
- **Custom Company Support**: For custom companies, the system tries common domain patterns
- **Fallback**: If logos fail to load, the interface gracefully degrades

#### Custom Company Logo Fetching
When you add a custom company, the system attempts to find logos by trying common domain patterns:
1. `companyname.com` (removes spaces, dots, hyphens)
2. `company-name.com` (spaces become hyphens)
3. `companyname.io` (for tech startups)

If a logo is found, it's automatically included in your flyer. If not, the company name appears without a logo.

### Custom Typography
The application uses the **Spicy Rice** font from [Google Fonts](https://fonts.googleapis.com/css2?family=Spicy+Rice&display=swap) to make names stand out:

- **Frontend Preview**: Uses web fonts loaded from Google Fonts CDN
- **Backend Generation**: Automatically downloads and caches the Spicy Rice font file
- **Fallback Handling**: If font download fails, gracefully falls back to system fonts

The font is downloaded once on server startup and cached locally for optimal performance.

### Modifying Flyer Design
Edit the `create_flyer` function in `backend/app.py` to customize:
- Colors and gradients
- Font sizes and styles
- Layout positioning
- Decorative elements

### Styling Changes
Modify `frontend/src/index.css` and `frontend/tailwind.config.js` to customize:
- Color schemes
- Typography
- Component styles
- Responsive breakpoints

## Production Deployment

### Backend
1. Set up a production WSGI server (e.g., Gunicorn)
2. Configure environment variables
3. Set up proper file storage
4. Add proper logging

### Frontend
1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Serve the `dist` folder with a web server
3. Update API endpoints to point to production backend

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on the GitHub repository.

---

**Made with ❤️ for the tech community** 