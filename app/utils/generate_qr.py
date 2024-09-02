import qrcode
import os

def generate_qr(id, data):
    qr_folder = f'app/static/img/qr/{data}'

    # Membuat direktori jika belum ada
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)
        print(f"Directory created: {qr_folder}")

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(id)
    qr.make(fit=True)

    # Convert QR code to image
    img = qr.make_image(fill_color="black", back_color="white")

    # Path lengkap untuk menyimpan file
    file_path = os.path.join(qr_folder, f'{id}.png')

    # Save image to the specified path
    img.save(file_path)
    print(f"QR Code saved to: {file_path}")

def delete_qr(id, data):
    qr_folder = f'app/static/img/qr/{data}'

    # Path lengkap untuk gambar QR code
    file_path = os.path.join(qr_folder, f'{id}.png')
    os.remove(file_path)