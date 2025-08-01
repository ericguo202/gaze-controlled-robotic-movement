# Instructions

To install the dependencies, please type the following in your terminal:

```bash
pip install -r requirements.txt
```

For the standard webpage and scripts, please open up the index.html file. After doing so, you will be prompted to allow access to your webcam. Allow access, and webgazer will begin calibrating immediately after you see the red dot appear on your screen.

In order to connect to the Websockets server, you must also type in your terminal the following command:
```bash
python app.py
```
or
```bash
python3 app.py
```
In the terminal, you should see "Connected to port 8765" if successful.

## Troubleshooting

If you are not prompted about your webcam, or the webcam shows up dark, please check that a webcam is connected. If so, open up a new terminal and type
```bash
python -m http.server 8080
```
In the terminal, you should see "Serving HTTP on :: port 8080 (http://[::]:8080/) ..." if successful.

Then, to open up the Websocket server, open up another new terminal (while keeping the other window open) and type:

```bash
python app.py
```
or
```bash
python3 app.py
```

In the terminal, you should see "Connected to port 8765" if successful.

In the browser, DO NOT open up the file. Instead, go to http://localhost:8080/index.html. Doing so should connect automatically to localhost:8765. If unsucessful, you should see an error message.

If successful, your browser will prompt you to allow access to your webcam.