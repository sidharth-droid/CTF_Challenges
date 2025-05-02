from PIL import Image
import piexif

def create_challenge():
    # Create a simple image
    img = Image.new('RGB', (100, 100), color='red')
    
    # Create EXIF data
    exif_dict = {
        "0th": {},
        "Exif": {},
        "GPS": {},
        "1st": {},
        "thumbnail": None
    }
    
    # Add the flag in a common EXIF field (like Image Description)
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = "flag{metadata_detective}".encode()
    
    # Convert EXIF dict to bytes
    exif_bytes = piexif.dump(exif_dict)
    
    # Save image with EXIF data
    img.save('secret.jpg', exif=exif_bytes)

if __name__ == '__main__':
    create_challenge()