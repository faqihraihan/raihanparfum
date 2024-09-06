import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def generate_qr(id, data, customer_name):
    qr_folder = f'../static/img/qr/{data}'

    current_dir = Path(__file__).parent.absolute()
    abs_qrfolder = current_dir / qr_folder

    # Membuat direktori jika belum ada
    if not os.path.exists(abs_qrfolder):
        os.makedirs(abs_qrfolder)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Menggunakan level koreksi error yang lebih tinggi
        box_size=10,
        border=4,
    )
    qr.add_data(id)
    qr.make(fit=True)

    # Convert QR code to image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Open the logo image
    logo_path = '../static/img/logo-raihan-parfum.png'

    current_dir = Path(__file__).parent.absolute()
    abs_logopath = current_dir / logo_path

    logo = Image.open(abs_logopath)
    
    # Resize the logo to fit within the QR code
    qr_width, qr_height = qr_img.size
    logo_size = qr_width // 5  # Memperbesar logo agar lebih terlihat
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Calculate the position to place the logo
    logo_x = (qr_width - logo_size) // 2
    logo_y = (qr_height - logo_size) // 2

    # Paste the logo onto the QR code with transparency mask
    qr_img.paste(logo, (logo_x, logo_y), logo)

    # Create a new image with space for text
    font_size = 20
    font_path = '../static/font/SourceSans3-Regular.ttf'

    current_dir = Path(__file__).parent.absolute()
    abs_fontpath = current_dir / font_path

    font = ImageFont.truetype(abs_fontpath, font_size)  # Menggunakan font TrueType

    text_img = Image.new('RGB', (qr_width, qr_height + font_size + 10), 'white')
    text_img.paste(qr_img, (0, 0))
    draw = ImageDraw.Draw(text_img)

    # Calculate text size
    text_bbox = draw.textbbox((0, 0), customer_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]

    # Center the text
    text_position = ((qr_width - text_width) // 2, qr_height - 15)  # Centered text with some padding

    # Draw the text
    draw.text(text_position, customer_name, fill="black", font=font)

    # Path lengkap untuk menyimpan file
    file_path = os.path.join(abs_qrfolder, f'{id}.png')

    # Save image to the specified path
    text_img.save(file_path)

def delete_qr(id, data):
    qr_folder = f'../static/img/qr/{data}'

    current_dir = Path(__file__).parent.absolute()
    abs_qrfolder = current_dir / qr_folder

    # Path lengkap untuk gambar QR code
    file_path = os.path.join(abs_qrfolder, f'{id}.png')
    os.remove(file_path)