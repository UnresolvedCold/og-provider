from flask import Flask, send_file, request, render_template
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import base64
import io
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('link-preview.html')

@app.route('/og_image')
def og_image():
    title = request.args.get('title')

    # This is the recommended size as per opengraph.xyz
    width = 1200
    height = 630

    # Let's get our image 
    # response = requests.get('https://live.staticflickr.com/7504/16258492451_3a097a932a_k.jpg')
    # image = Image.open(BytesIO(response.content))   
    # image.thumbnail((width, height))      # This is how you resize an image

    image=Image.new('RGB', (width, height))

    # Draw the title on the image
    draw = ImageDraw.Draw(image)

    truetype_url = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Black.ttf?raw=true'
    r = requests.get(truetype_url, allow_redirects=True)
    font = ImageFont.truetype(io.BytesIO(r.content), 64)

    # Calculate the x and y positions to center the text
    x = (width - draw.textsize(title, font=font)[0] ) // 2
    y = (height - draw.textsize(title, font=font)[1]) // 2

    draw.text((x, y), title, font=font, fill=(255, 255, 0))

    # Save the image to a temporary file
    image.save('og_image.png')

    # Return the image
    return send_file('og_image.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=4000)
