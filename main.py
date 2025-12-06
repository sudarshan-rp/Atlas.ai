from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
import os
import logging
from pathlib import Path
import time
import aiofiles

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = '/tmp/uploads'
API_VERSION = os.environ.get('API_VERSION', '1.0.0')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title="Document Processing API",
    version=API_VERSION,
    description="API for processing uploaded documents"
)

@app.get("/")
async def home():
    """Root endpoint - API information"""
    return {
        "service": "Document Processing API",
        "version": API_VERSION,
        "environment": ENVIRONMENT,
        "status": "running",
        "endpoints": {
            "POST /process": "Process uploaded file",
            "GET /health": "Health check",
            "GET /": "API information"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint for load balancer"""
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": time.time(),
            "version": API_VERSION
        },
        status_code=200
    )

@app.post("/process")
async def process_file(file: UploadFile = File(...)):
    """
    Process uploaded file
    Expected: multipart/form-data with 'file' field
    Returns: JSON with status and filename
    """
    start_time = time.time()
    
    # Check if file is empty
    if not file.filename:
        logger.warning("Empty filename in request")
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )
    
    try:
        # Read file content to get size
        content = await file.read()
        file_size = len(content)
        
        # Check file size
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File too large. Maximum size is 16MB"
            )
        
        # Secure the filename (basic sanitization)
        filename = Path(file.filename).name
        
        # Save file temporarily
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(content)
        
        # Process file (placeholder - just get basic info)
        processing_time = time.time() - start_time
        
        logger.info(f"Successfully processed file: {filename}, size: {file_size} bytes")
        
        # Clean up temporary file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return {
            "status": "ok",
            "filename": filename,
            "file_size_bytes": file_size,
            "processing_time_seconds": round(processing_time, 3),
            "message": "File processed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file: {str(e)}"
        )

@app.exception_handler(413)
async def file_too_large_handler(request: Request, exc: Exception):
    """Handle file too large error"""
    return JSONResponse(
        status_code=413,
        content={
            "status": "error",
            "message": "File too large. Maximum size is 16MB"
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error"
        }
    )

if __name__ == '__main__':
    import uvicorn
    
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting Document Processing API v{API_VERSION} on port {port}")
    
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=port,
        reload=(ENVIRONMENT == 'development')
    )