import uvicorn
from alembic.command import upgrade
from alembic.config import Config

from app.main import app as fast_api_app


def setup_app():
    """setup pyinstaller app"""

    alembic_cfg = Config(file_="app/alembic.ini")
    upgrade(alembic_cfg, "head")
    uvicorn.run(app=fast_api_app)


if __name__ == "__main__":
    setup_app()
