# Edited Image Detetction

Uses Error Level Analysis, Connected Components Labelling and Union Find Algorithm to detect digitally edited images.

## Getting Started

To run the script on your machine you will have to follow these steps.
The entire code is built to run on Python v3.6.5+ and PIP v18.0+

### Dependencies

You will have to install the following dependencies using PIP (Package Management System for Python).
All dependencies can be installed using the following command.

```
pip3 install -r requirements.txt
```

### Setting up server

You will have to start the server using the following command in your terminal.

```
python3 app.py
```
By default the server will run on http://127.0.0.1:5000/

You can test the API by -
1. 'POST' request on the URL - http://127.0.0.1:5000/upload
2. 'Content-Type' as 'multipart/form-data'
3.  'image': value - JPEG/JPG File
4.  'url'  : value - URL of the image.
```
If both the keys are passed to the POST request, 'image' is given higher priority.
```

### Note
The above method will run on your local host, to run it on custom IP, use the following command.
```
cd /path/to/this/dir/
export FLASK_APP=app.py --host=0.0.0.0 (Your custom IP)
flask run
```
For any other issues with running the app, check the following link. (http://flask.pocoo.org/docs/1.0/quickstart/)


### Running the tests
The response recieved when an edited image is passed.
```
{
    "edited": true,
    "maxToTotalRatio": 86.66666666666667
}
```
The response recieved when an original image is passed.
```
{
    "edited": false,
    "maxToTotalRatio": 34.78260869565217
}
```
"edited" returns 'true' when "maxToTotalRatio" is above 80% (You can change this threshold)

## Built With

* [Pillow](https://pillow.readthedocs.io/en/5.3.x/) - Python Imaging Library
* [Flask](http://flask.pocoo.org) - Web Development

## Authors

* **Kevin Jain** - *Initial work* - [GitHub](https://github.com/thatsKevinJain)
* **Utkarsh Sharma** - *Big help and inspiration* - [GitHub](https://github.com/Utkarsh85)


