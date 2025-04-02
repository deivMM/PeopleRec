from PIL import Image, ImageDraw, ImageFont

x, y = 700, 700 
image = Image.new('RGB', (x, y), color=(205, 205, 205))

draw = ImageDraw.Draw(image)

x_perc, y_perc = 0.1, 0.1
x1, y1 = int(x * x_perc), int(y * y_perc)
x2, y2 = int(x * (1 - x_perc)), int(y * (1 - y_perc))

draw.rectangle([ (x1,y1) , (x2,y2)], fill=(138, 149, 151))

# Cargar la fuente
font = ImageFont.truetype('font/LEMONMILK-Bold.otf', 40)
text = "No Image Available"
text_color = (0, 0, 0)  # Negro

# Obtener las dimensiones del texto con textbbox()
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Calcular la posición centrada
position = ((x - text_width) // 2, (y - text_height) // 2)
draw.text(position, text, font=font, fill=text_color)

# Mostrar y guardar la imagen
# image.show()
image.save("image_00.png")
