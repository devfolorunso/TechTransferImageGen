from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import os
import io
import base64
from datetime import datetime
import json
import requests
import urllib.request
import tempfile

app = Flask(__name__)
CORS(app)

# Use temp directory for serverless environment
TEMP_DIR = tempfile.gettempdir()
UPLOAD_FOLDER = os.path.join(TEMP_DIR, 'uploads')
GENERATED_FOLDER = os.path.join(TEMP_DIR, 'generated')
FONTS_FOLDER = os.path.join(TEMP_DIR, 'fonts')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)
os.makedirs(FONTS_FOLDER, exist_ok=True)

# Load tech companies data
def load_companies():
    """Load tech companies data from JSON file"""
    try:
        # In serverless environment, read from the same directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        companies_file = os.path.join(current_dir, 'companies.json')
        
        if not os.path.exists(companies_file):
            # Try backend directory
            companies_file = os.path.join(current_dir, '..', 'backend', 'companies.json')
        
        with open(companies_file, 'r') as f:
            data = json.load(f)
            return data['companies']
    except (FileNotFoundError, json.JSONDecodeError):
        print("Warning: companies.json not found. Using fallback data.")
        return [
            {"name": "Google", "domain": "google.com"},
            {"name": "Apple", "domain": "apple.com"},
            {"name": "Microsoft", "domain": "microsoft.com"},
            {"name": "Amazon", "domain": "amazon.com"},
            {"name": "Meta", "domain": "meta.com"},
            {"name": "Netflix", "domain": "netflix.com"},
            {"name": "Airbnb", "domain": "airbnb.com"},
            {"name": "Uber", "domain": "uber.com"},
            {"name": "Spotify", "domain": "spotify.com"},
            {"name": "Twitter", "domain": "twitter.com"}
        ]

TECH_COMPANIES = load_companies()

def download_font(font_url, font_name):
    """Download font if not already present"""
    font_path = os.path.join(FONTS_FOLDER, font_name)
    if not os.path.exists(font_path):
        try:
            urllib.request.urlretrieve(font_url, font_path)
            print(f"Downloaded {font_name} font to {font_path}")
        except Exception as e:
            print(f"Failed to download {font_name} font: {e}")
            return None
    return font_path

def get_font(font_name, size):
    """Get font for the given size"""
    font_urls = {
        'SpicyRice-Regular.ttf': "https://fonts.gstatic.com/s/spicyrice/v27/uK_24rSEd-Uqwk4jY1RyGv8.ttf",
        'LilitaOne-Regular.ttf': "https://fonts.gstatic.com/s/lilitaone/v15/i7dOIFdwYjGaAMFtZd_QA1b4Md8.ttf"
    }
    
    if font_name in font_urls:
        font_path = download_font(font_urls[font_name], font_name)
        if font_path and os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception as e:
                print(f"Failed to load {font_name} font: {e}")
    
    # Fallback to default font
    return ImageFont.load_default()

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """Get list of tech companies for dropdowns with logos"""
    companies_with_logos = []
    for company in TECH_COMPANIES:
        companies_with_logos.append({
            'name': company['name'],
            'domain': company['domain'],
            'logo': f"https://logo.clearbit.com/{company['domain']}"
        })
    
    companies_with_logos.sort(key=lambda x: x['name'])
    return jsonify({'companies': companies_with_logos})

@app.route('/api/generate-flyer', methods=['POST'])
def generate_flyer():
    """Generate a tech transfer announcement flyer"""
    try:
        # Get form data
        name = request.form.get('name')
        former_company = request.form.get('former_company')
        new_company = request.form.get('new_company')
        role = request.form.get('role')
        announcement_text = request.form.get('announcement_text')
        date = request.form.get('date')
        
        # Get uploaded image
        profile_image = request.files.get('profile_image')
        
        if not all([name, former_company, new_company, role, announcement_text, date, profile_image]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Generate the flyer
        flyer_data = create_flyer(name, former_company, new_company, role, announcement_text, date, profile_image)
        
        return jsonify({
            'success': True,
            'image_data': flyer_data,
            'filename': f"{name.replace(' ', '_') if name else 'unnamed'}_tech_transfer.png"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_flyer(name, former_company, new_company, role, announcement_text, date, profile_image):
    """Create a tech transfer announcement flyer"""
    # Create canvas
    width, height = 800, 900
    background_color = (15, 23, 42)
    
    # Create image
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # Add circuit board pattern background
    circuit_color = (30, 58, 138)
    glow_color = (59, 130, 246)
    
    # Draw circuit board pattern
    for i in range(0, width, 40):
        draw.line([(i, 0), (i, height)], fill=circuit_color, width=1)
    for i in range(0, height, 40):
        draw.line([(0, i), (width, i)], fill=circuit_color, width=1)
    
    # Add glowing circuit nodes
    for i in range(8):
        x = (i * 100 + 50) % width
        y = (i * 120 + 60) % height
        draw.ellipse([x-6, y-6, x+6, y+6], fill=glow_color)
        draw.ellipse([x-3, y-3, x+3, y+3], fill=(147, 197, 253))
    
    # Load fonts
    golden_color = (255, 215, 0)
    header_font = get_font('LilitaOne-Regular.ttf', 36)
    name_font = get_font('LilitaOne-Regular.ttf', 70)
    announcement_font = get_font('LilitaOne-Regular.ttf', 56)
    role_font = get_font('LilitaOne-Regular.ttf', 54)
    company_font = get_font('LilitaOne-Regular.ttf', 60)
    
    # Header
    header_text = "TECH TRANSFER ANNOUNCEMENT"
    header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
    header_width = header_bbox[2] - header_bbox[0]
    header_x = (width - header_width) // 2
    draw.text((header_x, 40), header_text, font=header_font, fill=golden_color)
    
    # Profile image
    try:
        profile_img = Image.open(profile_image)
        profile_img = profile_img.convert('RGB')
        profile_size = 200
        profile_img = profile_img.resize((profile_size, profile_size))
        
        # Create circular mask
        mask = Image.new('L', (profile_size, profile_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([(0, 0), (profile_size, profile_size)], fill=255)
        
        profile_img.putalpha(mask)
        profile_x = (width - profile_size) // 2
        profile_y = 100
        
        # Create background circle
        bg_circle_size = profile_size + 20
        bg_circle_x = profile_x - 10
        bg_circle_y = profile_y - 10
        draw.ellipse([bg_circle_x, bg_circle_y, bg_circle_x + bg_circle_size, bg_circle_y + bg_circle_size], 
                    fill=(255, 255, 255, 50))
        
        # Paste profile image
        img.paste(profile_img, (profile_x, profile_y), profile_img)
        
    except Exception as e:
        print(f"Error processing profile image: {e}")
        # Draw placeholder circle
        circle_size = 200
        circle_x = (width - circle_size) // 2
        circle_y = 100
        draw.ellipse([circle_x, circle_y, circle_x + circle_size, circle_y + circle_size], 
                    fill=(100, 100, 100))
    
    # Name
    name_bbox = draw.textbbox((0, 0), name.upper(), font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (width - name_width) // 2
    draw.text((name_x, 320), name.upper(), font=name_font, fill=(255, 255, 255))
    
    # Companies section
    y_offset = 420
    
    # Company logos and names
    def get_company_logo(company_name):
        """Get company logo from Clearbit"""
        try:
            company_data = next((c for c in TECH_COMPANIES if c['name'] == company_name), None)
            if company_data:
                logo_url = f"https://logo.clearbit.com/{company_data['domain']}"
                response = requests.get(logo_url, timeout=5)
                if response.status_code == 200:
                    return Image.open(io.BytesIO(response.content))
        except Exception as e:
            print(f"Error fetching logo for {company_name}: {e}")
        return None
    
    # Former company
    former_logo = get_company_logo(former_company)
    former_y = y_offset
    
    if former_logo:
        former_logo = former_logo.resize((80, 80))
        former_logo_x = width // 4 - 40
        img.paste(former_logo, (former_logo_x, former_y))
        former_text_y = former_y + 90
    else:
        former_text_y = former_y
    
    # Former company text
    former_bbox = draw.textbbox((0, 0), former_company, font=company_font)
    former_text_width = former_bbox[2] - former_bbox[0]
    former_text_x = width // 4 - former_text_width // 2
    draw.text((former_text_x, former_text_y), former_company, font=company_font, fill=(255, 255, 255))
    
    # Arrow
    arrow_y = y_offset + 40
    arrow_start_x = width // 2 - 60
    arrow_end_x = width // 2 + 60
    draw.line([(arrow_start_x, arrow_y), (arrow_end_x, arrow_y)], fill=golden_color, width=8)
    # Arrow head
    draw.polygon([(arrow_end_x, arrow_y), (arrow_end_x - 20, arrow_y - 10), (arrow_end_x - 20, arrow_y + 10)], 
                fill=golden_color)
    
    # New company
    new_logo = get_company_logo(new_company)
    new_y = y_offset
    
    if new_logo:
        new_logo = new_logo.resize((80, 80))
        new_logo_x = 3 * width // 4 - 40
        img.paste(new_logo, (new_logo_x, new_y))
        new_text_y = new_y + 90
    else:
        new_text_y = new_y
    
    # New company text
    new_bbox = draw.textbbox((0, 0), new_company, font=company_font)
    new_text_width = new_bbox[2] - new_bbox[0]
    new_text_x = 3 * width // 4 - new_text_width // 2
    draw.text((new_text_x, new_text_y), new_company, font=company_font, fill=(255, 255, 255))
    
    # Announcement text
    announcement_bbox = draw.textbbox((0, 0), announcement_text, font=announcement_font)
    announcement_width = announcement_bbox[2] - announcement_bbox[0]
    announcement_x = (width - announcement_width) // 2
    draw.text((announcement_x, 620), announcement_text, font=announcement_font, fill=golden_color)
    
    # Role
    role_bbox = draw.textbbox((0, 0), role.upper(), font=role_font)
    role_width = role_bbox[2] - role_bbox[0]
    role_x = (width - role_width) // 2
    draw.text((role_x, 700), role.upper(), font=role_font, fill=(255, 255, 255))
    
    # Date
    date_text = f"Effective: {date}"
    date_bbox = draw.textbbox((0, 0), date_text, font=header_font)
    date_width = date_bbox[2] - date_bbox[0]
    date_x = (width - date_width) // 2
    draw.text((date_x, 800), date_text, font=header_font, fill=(200, 200, 200))
    
    # Convert to base64
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return base64.b64encode(img_buffer.read()).decode('utf-8')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# Vercel serverless handler
def handler(request):
    return app(request.environ, lambda status, headers: None)

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000) 