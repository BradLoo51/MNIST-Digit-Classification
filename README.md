# MNIST Digit Classifier

A web app where user draw a digit on a canvas, which is sent to a PyTorch model for classification

**Architecture:** Flask serves the static frontend which sends the drawing directly to a separate FastAPI backend. The backend runs the PyTorch model and returns a prediction. A setup is also made for running the backend service in Docker container. The uv.lock venv is using an outdated PyTorch version to compensate on my old GPU (NVIDIA GeForce GTX 1050 3 GB).

<img width="786" height="559" alt="Screenshot of FrontEnd" src="https://github.com/user-attachments/assets/1ba1d665-1d51-4562-851b-2151053e050d" />


## Frontend (Flask)

`main.py` only serves the page – it has no knowledge of the model or prediction logic. It is hosting in `http://localhost:5000`

Run it with:
```bash
python main.py
```

---

## Backend (FastAPI)

Loads the PyTorch model once at startup and exposes a `/predict` POST endpoint

Run it locally with:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Docker (FastAPI backend)

**Dockerfile (CPU):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t <Docker Name> (eg. mnist-digit-classifier)
docker run -p 8000:8000 <Docker Name>
```
