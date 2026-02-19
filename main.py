from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeSubmission(BaseModel):
    language: str
    code: str

@app.post("/run")
async def run_code(submission: CodeSubmission):
    lang = submission.language.lower()
    code = submission.code
    unique_id = str(uuid.uuid4())[:8]
    temp_files = []

    try:
        # --- PYTHON ---
        if lang == "python":
            result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=10)
            return {"output": result.stdout or result.stderr}

        # --- C LANGUAGE ---
        elif lang == "c":
            filename = f"temp_{unique_id}.c"
            exe_name = f"temp_{unique_id}.exe"
            temp_files.extend([filename, exe_name])
            with open(filename, "w") as f: f.write(code)
            
            compile_res = subprocess.run(["gcc", filename, "-o", exe_name], capture_output=True, text=True)
            if compile_res.returncode != 0:
                return {"output": "Compilation Error:\n" + compile_res.stderr}
            
            run_res = subprocess.run([f"./{exe_name}"], capture_output=True, text=True, timeout=10)
            return {"output": run_res.stdout or run_res.stderr}

        # --- JAVA ---
        elif lang == "java":
            filename = "Main.java" # User must use 'public class Main'
            temp_files.extend([filename, "Main.class"])
            with open(filename, "w") as f: f.write(code)
            
            compile_res = subprocess.run(["javac", filename], capture_output=True, text=True)
            if compile_res.returncode != 0:
                return {"output": "Compilation Error:\n" + compile_res.stderr}
            
            run_res = subprocess.run(["java", "Main"], capture_output=True, text=True, timeout=10)
            return {"output": run_res.stdout or run_res.stderr}

        # --- JAVASCRIPT ---
        elif lang == "javascript":
            result = subprocess.run(["node", "-e", code], capture_output=True, text=True, timeout=10)
            return {"output": result.stdout or result.stderr}

        # --- HTML / CSS ---
        # These don't "run" on a server; they render in the browser. 
        # We will handle these in the frontend section below.
        elif lang in ["html", "css"]:
            return {"output": "HTML/CSS rendered in the preview window above!"}

        return {"output": f"Language {lang} not supported yet."}

    except Exception as e:
        return {"output": f"System Error: {str(e)}"}
    finally:
        for f in temp_files:
            if os.path.exists(f): os.remove(f)