from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.database import SessionLocal
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/health")
def health_check():
    db_status = "ok"
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except SQLAlchemyError:
        db_status = "error"

    overall = "ok" if db_status == "ok" else "degraded"
    return {"status": overall, "database": db_status}
