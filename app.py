import os

from flask import Flask, render_template, request, redirect

from inference import get_prediction
from commons import format_class_name
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/', methods=['GET'])
def home() :
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)

        if 'file' not in request.files:
            print("redirection")
            return redirect(request.url)
        classIds = []
        classNames = []
        filenames = []
        respObj = {}
        for uploaded_file in request.files.getlist('file'):


            img_bytes = uploaded_file.read()
            class_id, class_name = get_prediction(image_bytes=img_bytes)
            file_name = uploaded_file.filename
            if (type(class_name) == "string" or class_name in [0, 1, 2, 3, 4, 5]):
                tempClasse = class_name
                class_name = class_id
                class_id = tempClasse

            uploads_dir = os.path.join(app.static_folder, class_name)
            filename = secure_filename(file_name)
            uploaded_file.save(os.path.join(uploads_dir, filename))
            
            print(class_name)
            if  class_name in respObj.keys() :
                respObj[class_name].append({"class_id": class_id, "class_name": class_name, "file_name": file_name})
            else :
                respObj[class_name] = []
                respObj[class_name].append({"class_id": class_id, "class_name": class_name, "file_name": file_name})


        print(respObj.keys())
        return render_template('result.html', respObj= respObj)
    


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
