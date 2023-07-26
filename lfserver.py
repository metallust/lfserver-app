import os
from flask import Flask, request, render_template, send_file, redirect
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

app = Flask(__name__)

# Configure Flask to use the absolute paths
app.template_folder = 'C:/Users/IRFAN/Desktop/python/CS50AI/CS50p Final project/lfserver app/templates'
app.static_folder = 'C:/Users/IRFAN/Desktop/python/CS50AI/CS50p Final project/lfserver app/static'


@app.route("/")
def index():
    message = request.args.get("message")
    dirs = os.listdir(os.getcwd())
    context = []
    for files in dirs:
        temp = {}
        temp['isfile'] = os.path.isfile(files)
        temp["name"] = files
        temp["size"] = os.path.getsize(os.path.join(os.getcwd(), files))
        temp["upload_date"] = os.path.getmtime(os.path.join(os.getcwd(), files))
        temp['username'] = "None"
        context.append(temp)
    return render_template("index.html", files=context, folder=os.getcwd(),message=message)


@app.route("/upload", methods=["POST"])
def upload():
    uploaded_files = request.files.getlist("file")
    for file in uploaded_files:
        file.save(file.filename)

    return redirect("/?message=Files uploaded successfully")

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_file(os.path.join(os.getcwd(), filename), as_attachment=True)

@app.route("/open/<filename>", methods=["GET"])
def openfolder(filename):
    os.chdir(os.path.join(os.getcwd(), filename))
    return redirect('/?message=Folder opened')

@app.route("/close", methods=["GET"])
def close():
    os.chdir(os.path.join(os.getcwd(), ".."))
    return redirect('/?message=Folder closed')


if __name__ == "__main__":
    # run the app
    app.run(host=ip_address, port=5000, debug=False)
