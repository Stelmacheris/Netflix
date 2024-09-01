import uvicorn

host="127.0.0.1"
port=8002
app_name="app.main:app"


if __name__ == '__main__':
    uvicorn.run(app_name, host=host, port=port)