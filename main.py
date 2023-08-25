import uvicorn
from subprocess import run
from config.conf import settings


def main():
    """
    """
    if settings.mode_prod:
        run(f"gunicorn config.app:application -w {settings.workers} -b 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker".split(' '))
    else:
        uvicorn.run(
            "config.app:application",
            host="0.0.0.0",
            port=8000,
            reload=True,
        )


if __name__ == "__main__":
    main()
