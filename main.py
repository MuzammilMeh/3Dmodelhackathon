from gradio_client import Client
import shutil
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import requests
# Assuming you have imported the necessary libraries

app = FastAPI()

@app.get("/get_model/{prompt}")
async def get_model_endpoint(prompt: str, filename: str, seed: int = 1, guidance: int = 16, steps: int = 64):
    try:
        client = Client("https://hysts-shap-e.hf.space/")
        result = client.predict(
            prompt,
            seed,
            guidance,
            steps,
            api_name="/text-to-3d",
        )
        if result:
            project_directory = "models"
            output_filename = f"{filename}.glb"

            output_path = os.path.join(project_directory, output_filename)
            if os.path.exists(result):
                shutil.move(result, output_path)
                return FileResponse(output_path, media_type="application/octet-stream", filename=output_filename)
            else:
                raise HTTPException(status_code=500, detail="Prediction successful, but no valid result file received.")
        else:
            raise HTTPException(status_code=500, detail="Prediction failed or no result received.")
    except requests.exceptions.RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"An error occurred during the request: {req_err}")
    except TimeoutError as timeout_err:
        raise HTTPException(status_code=500, detail=f"Request timed out: {timeout_err}")
    except Exception as general_err:
        raise HTTPException(status_code=500, detail=f"An error occurred: {general_err}")

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)