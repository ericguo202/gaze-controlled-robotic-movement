# Instructions

To install the dependencies, please type the following in your terminal:

```bash
pip install -r requirements.txt
```

First, to ensure OpenCV works, open up a new terminal and type
```bash
python -m http.server 8080
```
In the terminal, you should see "Serving HTTP on :: port 8080 (http://[::]:8080/) ..." if successful.

Then, to open up the Websocket server, open up another new terminal (while keeping the other window open) and type:

```bash
python app.py
```

In the terminal, you should see "Connected to port 8765" if successful.

In the browser, DO NOT open up the file. Instead, go to http://localhost:8080/combined.html. Doing so should connect automatically to localhost:8765. If unsucessful, you should see an error message.

If successful, your browser will prompt you to allow access to your webcam.