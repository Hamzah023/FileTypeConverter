from fastapi import FastApi, File, UploadFile
from fastapi.responses import FileResponse
import os
import subprocess
import uuid

app = FastApi()

UPLOAD_DIR = "../uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True) #exists_ok=True creates the directory if it doesn't exist


@app.post("/convert")
async def convertPagesToPdf(file: UploadFile = File(...)): #the ... means that the file is required

    if not file.filename.endswith(".pages"):
        return {"error": "File must be a .pages file"}
        
    #save the fileName to a variable
    theFileName = file.filename

    fileId = str(uuid.uuid4()) 


    inputPath = f"{UPLOAD_DIR}/{fileId}.pages" 
    outputPath = f"{UPLOAD_DIR}/{fileId}.pdf" #outputPath is the path where the converted file will be saved

    with open(inputPath, "wb") as f: # open the file in binary write mode
        f.write(await file.read()) # read the contents of the uploaded file and write it to the new file inputPath

    #AppleScript command to convert .pages to .pdf
    script = f'''
    tell application "Pages"
        open POSIX file "{os.path.abspath(inputPath)}"
        delay 1
        set theDoc to front document
        export theDoc to POSIX file "{os.path.abspath(outputPath)}" as PDF
        close theDoc saving no
    end tell
    '''

    result = subprocess.run(["osascript", "-e", script], capture_output = True, text=True)

    if result.returncode != 0:
        return {"error": "Failed to convert .pages to .pdf", "details": result.stderr}

    return FileResponse(path=outputPath, media_type="application/pdf", filename=f"{theFileName}.pdf")

