from PIL import Image, ImageDraw

def make(S, path):
    img = Image.new('RGB', (S, S), '#111827')
    d = ImageDraw.Draw(img)
    gold = '#d4af37'
    cy = S // 2
    # central bar
    bar_h = int(S * 0.07)
    d.rectangle([int(S*0.30), cy-bar_h//2, int(S*0.70), cy+bar_h//2], fill=gold)
    # outer plates
    w, h = int(S*0.10), int(S*0.36)
    for cx in (int(S*0.255), int(S*0.745)):
        d.rounded_rectangle([cx-w//2, cy-h//2, cx+w//2, cy+h//2], radius=int(S*0.03), fill=gold)
    # inner plates
    w2, h2 = int(S*0.075), int(S*0.24)
    for cx in (int(S*0.345), int(S*0.655)):
        d.rounded_rectangle([cx-w2//2, cy-h2//2, cx+w2//2, cy+h2//2], radius=int(S*0.025), fill=gold)
    img.save(path)
    print('wrote', path)

base = '/Users/ryojikakizaki/Desktop/health/app/'
make(192, base + 'icon-192.png')
make(512, base + 'icon-512.png')
