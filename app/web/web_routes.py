from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@router.get("/shop", response_class=HTMLResponse)
async def shop_page(request: Request):
    return templates.TemplateResponse("shop.html", {"request": request})

@router.get("/imprint", response_class=HTMLResponse)
async def imprint_page(request: Request):
    return templates.TemplateResponse("imprint.html", {"request": request})

@router.get("/user", response_class=HTMLResponse)
async def user_dashboard(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})

