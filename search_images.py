import urllib.request, re

url = 'https://en.wikipedia.org/wiki/Momordica_charantia'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
matches = re.findall(r'//upload\.wikimedia\.org/wikipedia/commons/[^\s"\']+\.jpg', html, re.IGNORECASE)
print("Bitter Gourd:", list(set(matches))[:3])
