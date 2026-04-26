import os
import django
import urllib.request
import tempfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrolink.settings')
django.setup()

from farmers.models import Vegetable
from django.core.files import File

IMAGE_MAP = {
    'Potato': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=600&auto=format&fit=crop',
    'Onion': 'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=600&auto=format&fit=crop',
    'Tomato': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&auto=format&fit=crop',
    'Green Chili': 'https://images.unsplash.com/photo-1588143213570-34e7f37cc4cb?w=600&auto=format&fit=crop',
    'Bitter Gourd': 'https://images.unsplash.com/photo-1561136594-7f68413baa99?w=600&auto=format&fit=crop',
    'Eggplant': 'https://images.unsplash.com/photo-1604550186989-6cb8f7d9ff10?w=600&auto=format&fit=crop',
    'Cauliflower': 'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=600&auto=format&fit=crop',
    'Cabbage': 'https://images.unsplash.com/photo-1596483488795-0211d73a7638?w=600&auto=format&fit=crop',
    'Cucumber': 'https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=600&auto=format&fit=crop',
    'Pumpkin': 'https://images.unsplash.com/photo-1506917728037-b6fb01ab75f8?w=600&auto=format&fit=crop',
    'Spinach': 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=600&auto=format&fit=crop',
    'Carrot': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=600&auto=format&fit=crop',
}

for name, url in IMAGE_MAP.items():
    try:
        veg = Vegetable.objects.get(name=name)
        if veg.image:
            print(f"Skipping {name}")
            continue
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with tempfile.NamedTemporaryFile(delete=True) as tf:
                tf.write(response.read())
                tf.flush()
                file_name = f"{name.lower().replace(' ', '_')}.jpg"
                veg.image.save(file_name, File(tf), save=True)
                print(f"Saved {name}")
    except Exception as e:
        print(f"Failed {name}: {e}")
