from PIL import Image

img = Image.new("RGB", (1920, 1080), (255, 255, 255))
# img = Image.open('shop_items/house/0.png')
man = Image.open('shop_items/man.png')
house = Image.open('shop_items/house/0.png')
shoes = Image.open('shop_items/shoes/0.png')
tshort = Image.open('shop_items/tshort/1.png')
hat = Image.open('shop_items/hat/1.png')


img.paste(man, (0, 0), man)
img.paste(shoes, (0, 0), shoes)
img.paste(tshort, (0, 0), tshort)
img.paste(hat, (0, 0), hat)
img.save(f"shop_items/result/1.png")