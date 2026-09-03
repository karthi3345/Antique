from PIL import Image, ImageDraw

img = Image.open('static/img/museum_gallery.jpg')
draw = ImageDraw.Draw(img)

# Center frame
draw.rectangle([470, 182, 470+84, 182+120], outline="red", width=3)
# Left frame
draw.rectangle([305, 197, 305+70, 197+100], outline="green", width=3)
# Right frame
draw.rectangle([640, 197, 640+70, 197+100], outline="blue", width=3)

img.save('static/img/museum_test.jpg')
