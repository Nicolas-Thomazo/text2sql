from fastapi import APIRouter

from text2sql.api.routes import health

router = APIRouter()
router.include_router(health.router, prefix="/health")
