from dotenv import load_dotenv

from app import app

if __name__ == "__main__":
    load_dotenv()
    app.run(host="127.0.0.1", port=5000, debug=True)
