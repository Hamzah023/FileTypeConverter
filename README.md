
# FileTypeConverter

A web application that converts `.pages` documents to `.pdf` documents using FastAPI and AppleScript.

---

## How It Works

### 1. Setting Up the Upload Directory

```python
UPLOAD_DIR = "../uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
```

**Purpose:**  
Ensures that an uploads directory exists one level above the `src` directory. This is where uploaded `.pages` files and converted `.pdf` files will be stored.  
`os.makedirs`: Creates the directory if it doesn't already exist. The `exist_ok=True` flag prevents errors if the directory already exists.

---

### 2. FastAPI Endpoint

```python
@app.post("/convert")
async def convertPagesToPdf(file: UploadFile = File(...)):
```

**Purpose:**  
Defines a POST endpoint `/convert` that accepts a `.pages` file as input.  
`file: UploadFile`: Represents the uploaded file. The `File(...)` indicates that this parameter is required.

---

### 3. File Validation

```python
if not file.filename.endswith(".pages"):
    return {"error": "File must be a .pages file"}
```

**Purpose:**  
Ensures that only `.pages` files are accepted. If the uploaded file does not have a `.pages` extension, an error response is returned.

---

### 4. Generating a Unique File ID

```python
fileId = str(uuid.uuid4())
```

**Purpose:**  
Generates a unique identifier for each uploaded file using `uuid4()`. This ensures that files do not overwrite each other.

---

### 5. Defining File Paths

```python
inputPath = f"{UPLOAD_DIR}/{fileId}.pages"
outputPath = f"{UPLOAD_DIR}/{fileId}.pdf"
```

**Purpose:**  
- `inputPath`: The path where the uploaded `.pages` file will be saved.
- `outputPath`: The path where the converted `.pdf` file will be saved.

---

### 6. Saving the Uploaded File

```python
with open(inputPath, "wb") as f:
    f.write(await file.read())
```

**Purpose:**  
Saves the uploaded `.pages` file to the `inputPath`.  
- `open(inputPath, "wb")`: Opens the file in binary write mode.
- `file.read()`: Reads the contents of the uploaded file asynchronously.
- `f.write(...)`: Writes the file contents to the specified path.

---

### 7. AppleScript for Conversion

```python
script = f'''
tell application "Pages"
    open POSIX file "{os.path.abspath(inputPath)}"
    delay 1
    set theDoc to front document
    export theDoc to POSIX file "{os.path.abspath(outputPath)}" as PDF
    close theDoc saving no
end tell
'''
```

**Purpose:**  
Automates the conversion of `.pages` files to `.pdf` using the macOS "Pages" application.

**Key Steps:**
- Opens the `.pages` file.
- Exports it as a `.pdf` to the specified `outputPath`.
- Closes the document without saving changes.

---

### 8. Executing the AppleScript

```python
result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
```

**Purpose:**  
Runs the AppleScript using the `osascript` command-line tool.  
- `capture_output=True`: Captures the output and error messages from the command.
- `text=True`: Ensures the output is returned as a string.

---

### 9. Error Handling

```python
if result.returncode != 0:
    return {"error": "Failed to convert .pages to .pdf", "details": result.stderr}
```

**Purpose:**  
Checks if the AppleScript execution failed (non-zero return code). If so, returns an error response with details from `stderr`.

---

### 10. Returning the Converted File

```python
return FileResponse(path=outputPath, media_type="application/pdf", filename=f"{theFileName}.pdf")
```

**Purpose:**  
Sends the converted `.pdf` file back to the client as a downloadable response.

**FileResponse:**
- `path=outputPath`: Specifies the file to send.
- `media_type="application/pdf"`: Sets the MIME type to `application/pdf`.
- `filename=f"{theFileName}.pdf"`: Sets the filename for the client.

---

## Requirements

- **macOS:** The application relies on the "Pages" application and AppleScript, which are macOS-specific.
- **Python 3.9+:** Required for running FastAPI and the script.

---

## How to Run

1. Install dependencies:

```bash
pip install fastapi uvicorn
```

2. Start the FastAPI server:

```bash
uvicorn fileConversion:app --reload
```

3. Use a tool like **Postman** or **curl** to upload a `.pages` file to the `/convert` endpoint.

---

## Example Request

**Request:**

```bash
curl -X POST "http://127.0.0.1:8000/convert" \
-H "Content-Type: multipart/form-data" \
-F "file=@example.pages"
```

**Response:**

- If successful, the server will return the converted `.pdf` file.
- If an error occurs, the server will return a JSON response with the error details.

---

## Notes

- Ensure the "Pages" application is installed and accessible on your macOS system.
- The `uploads` directory must have appropriate write permissions.

---

✅ That's it — the entire README is clean, Markdown-formatted, and copy-paste ready.

---
