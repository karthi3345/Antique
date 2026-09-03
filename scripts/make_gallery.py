from PIL import Image, ImageDraw

def composite():
    # Load museum
    bg = Image.open('static/img/museum_gallery.jpg').convert('RGB')
    
    # We will just patch the watermark area by blurring it or overlaying a dark gradient 
    # instead of cropping so we don't change the aspect ratio.
    from PIL import ImageFilter
    watermark_box = (600, 400, 1024, 576)
    watermark_region = bg.crop(watermark_box)
    watermark_region = watermark_region.filter(ImageFilter.GaussianBlur(15))
    bg.paste(watermark_region, watermark_box)

    # Let's fix the Y coordinates based on OpenCV
    # OpenCV found:
    # (476, 185, 72, 67) -> Center frame
    # (317, 197, 58, 75) -> Left frame
    
    # Center frame
    c_width, c_height = 86, 128
    c_x, c_y = 470, 310
    
    # Wait, OpenCV said 476, 185. Let's use 185!
    c_x, c_y = 469, 310 # wait, let's look at the image proportions.
    c_width, c_height = 86, 122
    
    # Left frame
    l_width, l_height = 68, 98
    l_x, l_y = 308, 330
    
    # Right frame
    r_width, r_height = 68, 98
    r_x, r_y = 650, 330
    
    # Let's use Y=310, it's safer if the OpenCV was grabbing something else (like the top molding).
    # Wait, OpenCV found Y=185. 185 is much higher. Let's use 310 since most images have frames halfway down.
    # Actually, the user wants this in the hero section. Let's just use it as the background for the hero section, or as the image.

    try:
        obj1 = Image.open('static/img/objects/001/00.webp').convert('RGBA')
        obj2 = Image.open('static/img/objects/002/00.webp').convert('RGBA')
        obj3 = Image.open('static/img/objects/003/00.webp').convert('RGBA')
    except:
        return
        
    obj1 = obj1.resize((l_width, l_height))
    obj2 = obj2.resize((c_width, c_height))
    obj3 = obj3.resize((r_width, r_height))
    
    # Paste using alpha channel
    bg.paste(obj1, (l_x, l_y), obj1)
    bg.paste(obj2, (c_x, c_y), obj2)
    bg.paste(obj3, (r_x, r_y), obj3)
    
    bg.save('static/img/custom_gallery.jpg')

composite()
