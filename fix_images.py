import os
import django
import urllib.request
import tempfile
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrolink.settings')
django.setup()

from farmers.models import Vegetable
from django.core.files import File

IMAGE_MAP = {
    'Green Chili': 'https://upload.wikimedia.org/wikipedia/commons/5/50/Madame_Jeanette_and_other_chillies.jpg',
    'Cabbage': 'https://upload.wikimedia.org/wikipedia/commons/6/6f/Cabbage_and_cross_section_on_white.jpg',
    'Eggplant': 'https://upload.wikimedia.org/wikipedia/commons/7/76/Solanum_melongena_24_08_2012_%281%29.JPG',
    'Pumpkin': 'https://images.unsplash.com/photo-1506806732259-39c2d0268443?w=600',
    'Bitter Gourd': 'https://upload.wikimedia.org/wikipedia/commons/4/4f/Bittermelloncloseup.jpg',
}

def main():
    for name, url in IMAGE_MAP.items():
        try:
            veg = Vegetable.objects.get(name=name)
            
            print(f"Downloading image for {name} from {url}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with tempfile.NamedTemporaryFile(delete=True) as tf:
                    tf.write(response.read())
                    tf.flush()
                    file_name = f"{name.lower().replace(' ', '_')}.jpg"
                    
                    if veg.image:
                        veg.image.delete(save=False)
                        
                    veg.image.save(file_name, File(tf), save=True)
                    print(f"Successfully saved {file_name} for {name}")
            time.sleep(1) # delay to avoid rate limiting
        except Exception as e:
            print(f"Failed to process {name}: {e}")

if __name__ == '__main__':
    main()
