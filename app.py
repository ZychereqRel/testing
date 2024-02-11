from flask import Flask, render_template, request
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import json
from io import BytesIO
from PIL import Image
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET', 'POST'])
def main():
    result_text = ""

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            image_path = file.filename

            encoder = MultipartEncoder(
                fields={
                    'list_of_strings': '[]',
                    'image': (image_path, file.stream, 'image/png')
                }
            )

            headers = {
                'Content-Type': encoder.content_type,
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.7',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'sec-gpc': '1',
            }

            response = requests.post("https://us-central1-phaseoneai.cloudfunctions.net/locate_image", headers=headers, data=encoder)
            result_text = json.loads(response.text).get("message", "")

        elif 'url' in request.form:
            url = request.form['url']
            if url:
                try:
                    response = requests.get(url)
                    image = Image.open(BytesIO(response.content))
                    image_path = "image_from_url.png"
                    image.save(image_path)

                    encoder = MultipartEncoder(
                        fields={
                            'list_of_strings': '[]',
                            'image': (image_path, open(image_path, 'rb'), 'image/png')
                        }
                    )

                    headers = {
                        'Content-Type': encoder.content_type,
                        'accept': '*/*',
                        'accept-language': 'en-US,en;q=0.7',
                        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'cross-site',
                        'sec-gpc': '1',
                    }

                    response = requests.post("https://us-central1-phaseoneai.cloudfunctions.net/locate_image", headers=headers, data=encoder)
                    result_text = json.loads(response.text).get("message", "")

                except Exception as e:
                    result_text = f"Błąd podczas pobierania obrazu: {str(e)}"

    return render_template('main.html', result=result_text)

@app.route('/search', methods=['GET'])
def search():
    url = request.args.get('url', default="", type=str)
    if url:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image_path = "image_from_url.png"
            image.save(image_path)

            encoder = MultipartEncoder(
                fields={
                    'list_of_strings': '[]',
                    'image': (image_path, open(image_path, 'rb'), 'image/png')
                }
            )

            headers = {
                'Content-Type': encoder.content_type,
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.7',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'sec-gpc': '1',
            }

            response = requests.post("https://us-central1-phaseoneai.cloudfunctions.net/locate_image", headers=headers, data=encoder)
            result_text = json.loads(response.text).get("message", "")

        except Exception as e:
            result_text = f"Błąd podczas pobierania obrazu: {str(e)}"
    else:
        result_text = "Brak URL do przeszukania."

    return render_template('search.html', result=result_text)

if __name__ == '__main__':
    app.run(debug=True)
