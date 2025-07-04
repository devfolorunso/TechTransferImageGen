from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import os
import io
import base64
from datetime import datetime
import json
import requests
import urllib.request

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

# Load tech companies data from JSON file
def load_companies():
    """Load tech companies data from JSON file"""
    try:
        with open('companies.json', 'r') as f:
            data = json.load(f)
            return data['companies']
    except FileNotFoundError:
        print("Warning: companies.json not found. Using fallback data.")
        return [
            {"name": "Google", "domain": "google.com"},
            {"name": "Apple", "domain": "apple.com"},
            {"name": "Microsoft", "domain": "microsoft.com"},
            {"name": "Amazon", "domain": "amazon.com"},
            {"name": "Meta", "domain": "meta.com"}
        ]
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in companies.json")
        return []

# Load companies data
TECH_COMPANIES = load_companies()

# Font management
FONTS_FOLDER = 'fonts'
os.makedirs(FONTS_FOLDER, exist_ok=True)

def download_spicy_rice_font():
    """Download Spicy Rice font if not already present"""
    font_path = os.path.join(FONTS_FOLDER, 'SpicyRice-Regular.ttf')
    if not os.path.exists(font_path):
        try:
            # Download the Spicy Rice font from Google Fonts
            font_url = "https://fonts.gstatic.com/s/spicyrice/v27/uK_24rSEd-Uqwk4jY1RyGv8.ttf"
            urllib.request.urlretrieve(font_url, font_path)
            print(f"Downloaded Spicy Rice font to {font_path}")
        except Exception as e:
            print(f"Failed to download Spicy Rice font: {e}")
            return None
    return font_path

def download_lilita_one_font():
    """Download Lilita One font if not already present"""
    font_path = os.path.join(FONTS_FOLDER, 'LilitaOne-Regular.ttf')
    if not os.path.exists(font_path):
        try:
            # Download the Lilita One font from Google Fonts
            font_url = "https://fonts.gstatic.com/s/lilitaone/v15/i7dOIFdwYjGaAMFtZd_QA1b4Md8.ttf"
            urllib.request.urlretrieve(font_url, font_path)
            print(f"Downloaded Lilita One font to {font_path}")
        except Exception as e:
            print(f"Failed to download Lilita One font: {e}")
            return None
    return font_path

def get_spicy_rice_font(size):
    """Get Spicy Rice font for the given size"""
    font_path = download_spicy_rice_font()
    if font_path and os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception as e:
            print(f"Failed to load Spicy Rice font: {e}")
    
    # Fallback to system fonts
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

def get_lilita_one_font(size):
    """Get Lilita One font for the given size"""
    font_path = download_lilita_one_font()
    if font_path and os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception as e:
            print(f"Failed to load Lilita One font: {e}")
    
    # Fallback to system fonts
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

# Download fonts on startup
download_spicy_rice_font()
download_lilita_one_font()

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
    
    # Sort by name
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
        flyer_path = create_flyer(name, former_company, new_company, role, announcement_text, date, profile_image)
        
        # Return the generated image as base64
        with open(flyer_path, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image_data': img_data,
            'filename': f"{name.replace(' ', '_') if name else 'unnamed'}_tech_transfer.png"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_flyer(name, former_company, new_company, role, announcement_text, date, profile_image):
    """Create a tech transfer announcement flyer"""
    # Create canvas (reduced height)
    width, height = 800, 900  # Reduced from 1000 to 800
    background_color = (15, 23, 42)  # Dark navy blue
    
    # Create image
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # Add circuit board pattern background
    circuit_color = (30, 58, 138)  # Darker blue for circuit lines
    glow_color = (59, 130, 246)   # Bright blue for glowing effects
    
    # Draw circuit board pattern
    for i in range(0, width, 40):
        draw.line([(i, 0), (i, height)], fill=circuit_color, width=1)
    for i in range(0, height, 40):
        draw.line([(0, i), (width, i)], fill=circuit_color, width=1)
    
    # Add some diagonal circuit lines
    for i in range(0, width + height, 80):
        draw.line([(i, 0), (i - height, height)], fill=circuit_color, width=1)
        draw.line([(0, i), (width, i - width)], fill=circuit_color, width=1)
    
    # Add glowing circuit nodes
    for i in range(8):
        x = (i * 100 + 50) % width
        y = (i * 120 + 60) % height
        # Outer glow
        draw.ellipse([x-6, y-6, x+6, y+6], fill=glow_color)
        # Inner bright core
        draw.ellipse([x-3, y-3, x+3, y+3], fill=(147, 197, 253))
    
    # Load fonts first
    golden_color = (255, 215, 0)  # Gold color
    try:
        header_font = get_lilita_one_font(36)
        name_font = get_lilita_one_font(70)  # Increased from 48 to 64
        announcement_font = get_lilita_one_font(56)  # Increased from 42 to 56
        role_font = get_lilita_one_font(54)
        company_font = get_lilita_one_font(60)
        label_font = get_lilita_one_font(16)
    except:
        header_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        announcement_font = ImageFont.load_default()
        role_font = ImageFont.load_default()
        company_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    # Add header text "TRANSFER WINDATE UPDATE"
    header_text = "TRANSFER UPDATE"
    header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
    header_width = header_bbox[2] - header_bbox[0]
    draw.text(((width - header_width) // 2, 20), header_text, fill=golden_color, font=header_font)
    
    # Process profile image with golden border (increased size)
    profile_img = Image.open(profile_image)
    profile_size = (360, 360)  # Increased from 320x320 to 360x360
    profile_img = profile_img.resize(profile_size, Image.Resampling.LANCZOS)
    
    # Create circular mask for profile image
    mask = Image.new('L', profile_size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0] + list(profile_size), fill=255)
    
    # Create golden border background
    border_size = (profile_size[0] + 20, profile_size[1] + 20)
    border_bg = Image.new('RGBA', border_size, (255, 215, 0, 255))
    
    # Create inner circle mask for the border
    border_mask = Image.new('L', border_size, 0)
    border_mask_draw = ImageDraw.Draw(border_mask)
    border_mask_draw.ellipse([0, 0] + list(border_size), fill=255)
    
    # Paste profile image onto golden border
    profile_pos = ((border_bg.width - profile_size[0]) // 2, (border_bg.height - profile_size[1]) // 2)
    border_bg.paste(profile_img, profile_pos, mask)
    
    # Paste golden bordered profile onto main image
    img.paste(border_bg, (width//2 - border_bg.width//2, 80), border_mask)
    
    # Add company transition section with banner style
    company_y = 480  # Moved down from 330 to avoid overlapping with larger profile image
    banner_height = 120
    banner_color = (229, 231, 235)  # Light gray banner
    
    try:
        # Draw company banner background
        banner_rect = [50, company_y - 40, width - 50, company_y + banner_height - 40]
        draw.rectangle(banner_rect, fill=banner_color)
        
        # Get company logos
        def get_company_logo(company_name):
            """Get company logo from the companies list or try to fetch for custom companies"""
            # First check if company is in our predefined list
            for company in TECH_COMPANIES:
                if company['name'] == company_name:
                    try:
                        import requests
                        logo_url = f"https://logo.clearbit.com/{company['domain']}"
                        response = requests.get(logo_url, timeout=5)
                        if response.status_code == 200:
                            logo_img = Image.open(io.BytesIO(response.content))
                            logo_img = logo_img.resize((42, 42), Image.Resampling.LANCZOS)
                            return logo_img
                    except:
                        pass
                    break
            
            # If not in predefined list, try to fetch logo using company name as domain
            # This handles custom companies
            try:
                import requests
                # Try common domain patterns for custom companies
                possible_domains = [
                    f"{company_name.lower().replace(' ', '').replace('.', '').replace('-', '')}.com",
                    f"{company_name.lower().replace(' ', '-').replace('.', '').replace('_', '-')}.com",
                    f"{company_name.lower().replace(' ', '').replace('.', '').replace('-', '')}.io"
                ]
                
                for domain in possible_domains:
                    try:
                        logo_url = f"https://logo.clearbit.com/{domain}"
                        response = requests.get(logo_url, timeout=3)
                        if response.status_code == 200:
                            logo_img = Image.open(io.BytesIO(response.content))
                            logo_img = logo_img.resize((42, 42), Image.Resampling.LANCZOS)
                            return logo_img
                    except:
                        continue
            except:
                pass
            
            return None
        
        # Load company logos (increased size)
        former_logo = get_company_logo(former_company)
        new_logo = get_company_logo(new_company)
        
        # Resize logos to be bigger
        logo_size = 48  # Increased from 32
        if former_logo:
            former_logo = former_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        if new_logo:
            new_logo = new_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Use bigger company font
        bigger_company_font = get_lilita_one_font(34)  # Increased from 20
        
        # Draw company logos and names in banner
        logo_y = company_y + 5
        logo_text_gap = 15
        
        # Calculate positioning for centered layout with arrow
        former_text_bbox = draw.textbbox((0, 0), former_company, font=bigger_company_font)
        former_text_width = former_text_bbox[2] - former_text_bbox[0]
        
        new_text_bbox = draw.textbbox((0, 0), new_company, font=bigger_company_font)
        new_text_width = new_text_bbox[2] - new_text_bbox[0]
        
        # Calculate sections
        former_section_width = (logo_size + logo_text_gap if former_logo else 0) + former_text_width
        new_section_width = (logo_size + logo_text_gap if new_logo else 0) + new_text_width
        arrow_width = 30
        
        total_width = former_section_width + arrow_width + new_section_width + 60  # 60 for spacing
        start_x = (width - total_width) // 2
        
        # Former company section (left side)
        current_x = start_x
        if former_logo:
            img.paste(former_logo, (current_x, logo_y), former_logo if former_logo.mode == 'RGBA' else None)
            current_x += logo_size + logo_text_gap
        draw.text((current_x, logo_y + 12), former_company, fill=(0, 0, 0), font=bigger_company_font)
        current_x += former_text_width + 30
        
        # Arrow in center
        try:
            arrow_font = ImageFont.truetype("arial.ttf", 36)  # Bigger arrow
        except:
            arrow_font = ImageFont.load_default()
        draw.text((current_x, logo_y + 10), "→", fill=(0, 0, 0), font=arrow_font)
        current_x += arrow_width + 30
        
        # New company section (right side)
        if new_logo:
            img.paste(new_logo, (current_x, logo_y), new_logo if new_logo.mode == 'RGBA' else None)
            current_x += logo_size + logo_text_gap
        draw.text((current_x, logo_y + 12), new_company, fill=(0, 0, 0), font=bigger_company_font)
        
        # Add name in golden text
        name_bbox = draw.textbbox((0, 0), name.upper(), font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        draw.text(((width - name_width) // 2, 620), name.upper(), fill=golden_color, font=name_font)
        
        # Add announcement text in golden (with more spacing)
        announcement_bbox = draw.textbbox((0, 0), announcement_text, font=announcement_font)
        announcement_width = announcement_bbox[2] - announcement_bbox[0]
        draw.text(((width - announcement_width) // 2, 710), announcement_text, fill=golden_color, font=announcement_font)
        
        # Add role text in golden (with more spacing) - COMMENTED OUT
        # role_bbox = draw.textbbox((0, 0), role, font=role_font)
        # role_width = role_bbox[2] - role_bbox[0]
        # draw.text(((width - role_width) // 2, 770), role, fill=golden_color, font=role_font)
        
    except Exception as e:
        print(f"Error adding text: {e}")
        # Fallback text with golden color
        fallback_header_font = get_lilita_one_font(36)
        fallback_name_font = get_lilita_one_font(70)  # Updated to match main font
        fallback_announcement_font = get_lilita_one_font(56)  # Updated to match main font
        fallback_role_font = get_lilita_one_font(54)  # Updated to match main font
        
        # Add fallback elements
        draw.text((width//2 - 200, 20), "TRANSFER WINDATE UPDATE", fill=golden_color, font=fallback_header_font)
        draw.text((width//2 - 150, 620), name.upper(), fill=golden_color, font=fallback_name_font)
        draw.text((width//2 - 100, 710), announcement_text, fill=golden_color, font=fallback_announcement_font)
        # draw.text((width//2 - 50, 770), role, fill=golden_color, font=fallback_role_font)  # COMMENTED OUT
    
    # Save the image
    filename = f"{name.replace(' ', '_')}_tech_transfer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(GENERATED_FOLDER, filename)
    img.save(filepath)
    
    return filepath

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 