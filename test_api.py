from fastapi.testclient import TestClient
from imaginairy.http_app.app import app

client = TestClient(app)

response = client.post(
    "/api/generate_ui",
    json={
        "prompt": "a red apple",
        "model": "Stable Diffusion 1.5",
        "image_size": "256 × 256",
        "steps": 2,
        "controlnet": "None"
    }
)

print(response.status_code)
print(response.json())
