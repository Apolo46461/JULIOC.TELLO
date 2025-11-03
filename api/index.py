from app import app

# Vercel expects the app to be exported as a WSGI application
application = app

if __name__ == "__main__":
    app.run()
