from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as authRouter
from app.settings import settings
from app.user import router as userRouter
from app.mess import router as messRouter
from app.products import add as productAddRouter,get as productGetRouter

app = FastAPI(
    title="Your API Title",
    version="1.0.0",
    description="Backend API for your project",
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,         # e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(authRouter, prefix="/auth", tags=["Auth"])
app.include_router(userRouter, prefix="/user", tags=["User"])
app.include_router(messRouter, prefix="/mess", tags=["Mess"])
app.include_router(router=productAddRouter, prefix="/product", tags=["Product"])
app.include_router(router=productGetRouter, prefix="/product", tags=["Product"])

# Root Endpoint
@app.get("/", tags=["Root"])
async def get_root():
    return {"message": "It's working"}
