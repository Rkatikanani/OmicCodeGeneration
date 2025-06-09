from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
print("Environment variables loaded")
print(f"OPENAI_API_KEY exists: {bool(os.getenv('OPENAI_API_KEY'))}")

app = FastAPI(
    title="Omic Code Generation API",
    description="API for generating omic analysis code from natural language",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeGenerationRequest(BaseModel):
    natural_language: str
    analysis_type: Optional[str] = None
    context: Optional[dict] = None

class CodeGenerationResponse(BaseModel):
    generated_code: str
    explanation: str
    metadata: Optional[dict] = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment variables.")
openai.api_key = OPENAI_API_KEY

@app.get("/")
async def root():
    return {"message": "Welcome to Omic Code Generation API"}

@app.post("/generate-code", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    try:
        # Compose the prompt for ChatGPT
        system_prompt = (
            "You are an expert bioinformatics assistant. "
            "Given a natural language description of an omic analysis task, "
            "generate the appropriate code (in R or Python) to perform the analysis. "
            "Explain your reasoning and any assumptions. "
            "If a context or analysis type is provided, use it to inform your response."
        )
        user_prompt = f"Task: {request.natural_language}\n"
        if request.analysis_type:
            user_prompt += f"Analysis type: {request.analysis_type}\n"
        if request.context:
            user_prompt += f"Context: {request.context}\n"
        user_prompt += "\nPlease provide only the code and a brief explanation."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=800,
            temperature=0.2
        )
        content = response.choices[0].message.content
        # Try to split code and explanation
        if '```' in content:
            parts = content.split('```')
            explanation = parts[0].strip()
            code = parts[1].strip()
        else:
            explanation = content
            code = ""
        return CodeGenerationResponse(
            generated_code=code,
            explanation=explanation,
            metadata={"model": "gpt-3.5-turbo"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis-types")
async def get_analysis_types():
    # TODO: Implement actual analysis types
    return {
        "analysis_types": [
            "RNA-seq",
            "DNA-seq",
            "Proteomics",
            "Metabolomics",
            "Single-cell"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 