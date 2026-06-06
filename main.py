from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from youtube_api import get_comments
from sentiment import analyze_sentiment

app = FastAPI(title="YouTube Sentiment API")

# UI setup
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
def analyze(request: Request, video_id: str = Form(...)):
    comments = get_comments(video_id)
    
    results = []
    for comment in comments:
        sentiment = analyze_sentiment(comment)
        results.append({
            "comment": comment,
            "sentiment": sentiment
        })

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": results,
            "video_id": video_id
        }
    )


# Optional API endpoint (for REST testing)
@app.get("/api/sentiment/{video_id}")
def api_sentiment(video_id: str):
    comments = get_comments(video_id)
    
    data = []
    for c in comments:
        data.append({
            "comment": c,
            "sentiment": analyze_sentiment(c)
        })
    
    return {"video_id": video_id, "analysis": data}