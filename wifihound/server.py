"""FastAPI application factory and static-file serving."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from wifihound import __version__
from wifihound.api import router

WEB_DIR = Path(__file__).parent / "web"


@asynccontextmanager
async def _lifespan(app: FastAPI):
    yield
    # Graceful shutdown (Ctrl+C or the /api/shutdown route): stop any live
    # capture so airodump-ng is killed and the interface is restored to managed
    # mode instead of being left in monitor mode.
    try:
        from wifihound.api.routes import CAPTURE
        await CAPTURE.stop()
    except Exception:
        pass


def create_app() -> FastAPI:
    app = FastAPI(title="WiFiHound", version=__version__, lifespan=_lifespan)
    app.include_router(router)

    app.mount(
        "/static",
        StaticFiles(directory=str(WEB_DIR / "static")),
        name="static",
    )

    @app.get("/")
    def index():
        return FileResponse(str(WEB_DIR / "index.html"))

    @app.get("/favicon.ico", include_in_schema=False)
    def favicon():
        # Serve the icon for browsers that request /favicon.ico at the site root.
        # no-cache so a refreshed icon is picked up instead of a stale cached one.
        return FileResponse(
            str(WEB_DIR / "static" / "img" / "favicon.ico"),
            headers={"Cache-Control": "no-cache"},
        )

    @app.get("/health")
    def health():
        return {"status": "ok", "version": __version__}

    return app


app = create_app()
