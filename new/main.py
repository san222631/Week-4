from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key_here")
templates = Jinja2Templates(directory="templates")

@app.post("/signin")
async def handle_login(request: Request, username: str = Form(None), password: str = Form(None)):
    if not username or not password:
        return RedirectResponse(url='/error?message=Please enter username and password', status_code=303)
    if username == "test" and password == "test":
        request.session['signed_in'] = True
        return RedirectResponse(url='/member', status_code=303)
    else:
        request.session.clear()
        return RedirectResponse(url='/error?message=帳號、或密碼輸入錯誤', status_code=303)

@app.get("/signout")
async def signout(request: Request):
    request.session['signed_in'] = False
    return RedirectResponse(url='/', status_code=303)

@app.get("/member")
async def member_page(request: Request):
    if request.session.get('signed_in'):
        response = FileResponse('templates/member.html')
        response.headers['Cache-Control'] = 'no-store'
        return response
    else:
        return RedirectResponse(url='/', status_code=303)    

@app.get("/error")
async def error_page(request: Request):
    message = request.query_params.get('message', 'Unknown error')
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})






