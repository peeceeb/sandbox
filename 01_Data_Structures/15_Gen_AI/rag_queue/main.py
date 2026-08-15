from dotenv import load_dotenv
import uvicorn

try:
    from .server import app
except ImportError:
    from server import app

load_dotenv()


def main():
    uvicorn.run(app, port=8000, host="0.0.0.0")


if __name__ == "__main__":
    main()