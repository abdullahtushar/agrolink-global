import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrolink.settings')
django.setup()

from farmers.models import Vegetable
from django.core.files import File

def main():
    try:
        veg = Vegetable.objects.get(name='Pumpkin')
        image_path = r'C:\Users\ASUS\.gemini\antigravity\brain\04f44ee4-c56b-452f-9a9d-80f239123ee4\media__1777200726818.jpg'
        
        with open(image_path, 'rb') as f:
            if veg.image:
                veg.image.delete(save=False)
            veg.image.save('pumpkin_custom.jpg', File(f), save=True)
            
        print("Successfully updated Pumpkin image!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
