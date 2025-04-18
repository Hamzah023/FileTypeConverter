# Save the uploaded file
# uuid() converts it to a string and uuid4() generates a 
# random UUID, a UUID is a universally unique identifier,
# for example: 123e4567-e89b-12d3-a456-426614174000

# When a .pages file is uploaded via the /convert endpoint, 
# the server generates a unique fileId and uses this line 
# to determine where the uploaded file will be saved in the 
# uploads directory. This ensures that each file has a unique 
# path and avoids conflicts.

# the subprocess.run() function is used to run the AppleScript command
# The capture_output=True argument captures the output of the command
# The text=True argument makes the output a string instead of bytes
# the -e argument is used to specify the applescript command to be passed as a single line
# the osascript command is a command line tool thats used to execute AppleScript scripts 

# Explanation: return FileResponse(path=outputPath, media_type="application/pdf", filename=f"{theFileName}.pdf")

# FileResponse:

# This is a FastAPI utility that allows you to send a file as a response to the client. It is used to serve files (e.g., PDFs, images) in HTTP responses.

# path=outputPath:

# Specifies the file path of the PDF file to be sent in the response. In this case, outputPath is the location where #the converted .pdf file was saved.

# media_type="application/pdf":

# Sets the MIME type of the response to application/pdf, indicating that the file being sent is a PDF document.

# filename=f"{theFileName}.pdf":

# Specifies the name of the file that the client will see when downloading it. It uses the original file name #(theFileName) with a .pdf extension.

# This code snippet:

# with open(inputPath, "wb") as f: # open the file in binary write mode
#     f.write(await file.read()) # read the contents of the uploaded file and write it to the new file

# Explanation:
# with open(inputPath, "wb") as f::

# open(inputPath, "wb"):
# Opens a file at the path specified by inputPath for writing in binary mode ("wb").
# If the file does not exist, it will be created.
# If the file already exists, its contents will be overwritten.
# with statement:
# Ensures that the file is properly closed after the block is executed, even if an exception occurs. This is a best practice for file handling in Python.
# f.write(await file.read()):

# file.read():
# Reads the entire content of the uploaded file (file), which is an instance of UploadFile from FastAPI.
# Since file.read() is an asynchronous operation, it is awaited using await.
# f.write(...):
# Writes the binary content read from the uploaded file into the newly opened file (f) at the specified inputPath.
# Purpose:
# This block of code saves the uploaded file (received via the FastAPI endpoint) to the server's filesystem at the location specified by inputPath. It ensures the # file is written in binary mode, which is necessary for non-text files like .pages.

