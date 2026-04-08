import traceback
from gradio_dashboard import recommend_books
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- INPUT FORMAT --------
class QueryRequest(BaseModel):
    query: str
    category: str = "All"
    tone: str = "All"

# -------- ENDPOINT --------
@app.post("/recommend")
def recommend(data: QueryRequest):
    try:
        results = recommend_books(data.query, data.category, data.tone)

        output = []
        for img, caption in results:
            try:
                title = caption.split(" by ")[0]
                author = caption.split(" by ")[1].split(":")[0]
                description = caption.split(":")[-1]
            except:
                title = caption
                author = "Unknown"
                description = caption

            output.append({
                "title": title,
                "author": author,
                "description": description,
                "image": img
            })

        return {"results": output}

    except Exception as e:
        traceback.print_exc()  # prints full error in your terminal
        return {"error": str(e)}