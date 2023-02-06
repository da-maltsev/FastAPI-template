from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from app.admin.models import VIEWS
from app.db.session import engine
from app.module.router import router as module_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="topsecret007")

admin = Admin(app, engine)
for view in VIEWS:
    admin.add_view(view)


@app.get("/", include_in_schema=False)
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse("/docs")


app.include_router(module_router)
