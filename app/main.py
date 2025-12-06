from flask import Flask, request, jsonify
import os
import logging
from werkzeug.utils import secure_filename
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment variables
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
API_VERSION = os.environ.get('API_VERSION', '1.0.0')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    """Root endpoint - API information"""
    return jsonify({
        "service": "Document Processing API",
        "version": API_VERSION,
        "environment": ENVIRONMENT,
        "status": "running",
        "endpoints": {
            "POST /process": "Process uploaded file",
            "GET /health": "Health check",
            "GET /": "API information"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint for load balancer"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "version": API_VERSION
    }), 200

@app.route('/process', methods=['POST'])
def process_file():
    """
    Process uploaded file
    Expected: multipart/form-data with 'file' field
    Returns: JSON with status and filename
    """
    start_time = time.time()
    
    # Check if file is in request
    if 'file' not in request.files:
        logger.warning("No file part in request")
        return jsonify({
            "status": "error",
            "message": "No file part in the request"
        }), 400
    
    file = request.files['file']
    
    # Check if file is empty
    if file.filename == '':
        logger.warning("Empty filename in request")
        return jsonify({
            "status": "error",
            "message": "No file selected"
        }), 400
    
    try:
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Get file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        # Save file temporarily (in production, you might process or upload to S3)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process file (placeholder - just get basic info)
        processing_time = time.time() - start_time
        
        logger.info(f"Successfully processed file: {filename}, size: {file_size} bytes")
        
        # Clean up temporary file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            "status": "ok",
            "filename": filename,
            "file_size_bytes": file_size,
            "processing_time_seconds": round(processing_time, 3),
            "message": "File processed successfully"
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to process file",
            "error": str(e)
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        "status": "error",
        "message": "File too large. Maximum size is 16MB"
    }), 413

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Document Processing API v{API_VERSION} on port {port}")
    app.run(host='0.0.0.0', port=port, debug=(ENVIRONMENT == 'development'))