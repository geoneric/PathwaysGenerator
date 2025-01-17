# Run the app

To run the app from within this directory:

```
flet run main.py
```

To run the app as a website:

```
flet run --web
```

To build the web app:

```
# Assumes you're in the binary directory
cmake --build . --target web_app

# Alternatively, if using Ninja for example
ninja web_app
```
