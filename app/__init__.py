from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as authRouter
from app.settings import settings
from app.user import router as userRouter
from app.mess import router as messRouter
from app.products import add as productAddRouter,get as productGetRouter
from app.order import add as orderAddRouter

app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
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
app.include_router(router=orderAddRouter, prefix="/order", tags=["Order"])

# Root Endpoint
@app.get("/", tags=["Root"])
async def get_root():
    return {"message": "It's working"}
