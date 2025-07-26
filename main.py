import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        "app:app",          # module:application
        host="0.0.0.0",     # bind to all interfaces
        port=1024,          # port to listen on
        reload=True         # enable auto-reload (development only)
    )
