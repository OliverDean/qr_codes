import qrcode
import sys
from PIL import Image

def create_qr_code(data, output_file):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img = img.convert("RGB")
    img.save(output_file)
    return img

def encode_hidden_message(image_path, message, block_size=10):
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = img.load()

    binary_message = message_to_binary(message)
    width, height = img.size
    message_index = 0

    darker = (30, 30, 50)

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            r, g, b = pixels[x, y]
            if (r, g, b) == (0, 0, 0):  # If the pixel is black
                if message_index < len(binary_message):
                    color = darker if binary_message[message_index] == '0' else (0, 0, 0)
                    for i in range(block_size):
                        for j in range(block_size):
                            if x + i < width and y + j < height:
                                pixels[x + i, y + j] = color
                    message_index += 1

    img.save(image_path)

def message_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python qr_with_steg.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = "qrcode_steg.png"
    create_qr_code(url, output_file)
    hidden_message = "PLEASE HIRE ME THANKYOU END"
    encode_hidden_message(output_file, hidden_message)
    
    print(f"QR code with hidden message saved as {output_file}")
