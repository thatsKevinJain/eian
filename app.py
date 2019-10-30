from flask import Flask, jsonify, request
import ImageELA
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
	url = None
	if request.method == 'POST':
		if 'image' in request.files:
			return jsonify(ImageELA.ELA(request.files['image'],1))
		elif 'url' in request.form:
				return jsonify(ImageELA.ELA(request.form['url'],2))
	return error
if __name__ == "__main__":
    app.run()
