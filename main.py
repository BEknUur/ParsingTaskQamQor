from fastapi import FastAPI, HTTPException, Query
import httpx
from pydantic import BaseModel
from typing import Union

app = FastAPI(title="QamqorParser API")

#простое решение задачи это просто заходить на сайт и взять токен капчи из кода страницы 
CAPTCHA_STUB = "введите recaptcha token"


TIMEOUT = 30.0
BASE_URL = "https://qamqor.gov.kz/api/public/person_case"


class SearchResponse(BaseModel):
    data: Union[dict, None]
    code: str
    status: str
    time: str

async def solve_captcha():
  
    return CAPTCHA_STUB

async def search_by_last_name(last_name: str, page: int = 0):
    
    captcha_token = await solve_captcha()
    
 
    async with httpx.AsyncClient(timeout=TIMEOUT, verify=False) as client:
        encoded_name = f"*{last_name}*"
        
        url = f"{BASE_URL}/criminal"
        params = {
            "page": page,
            "last_name": encoded_name,
            "re_captcha": captcha_token
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        response = await client.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code)
        
        return response.json()

async def search_by_iin(iin: str, page: int = 0):
    captcha_token = await solve_captcha()

    async with httpx.AsyncClient(timeout=TIMEOUT, verify=False) as client:
        url = f"{BASE_URL}/criminal"
        params = {
            "page": page,
            "iin": iin,
            "re_captcha": captcha_token
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = await client.get(url, params=params, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code)

        data = response.json()

        if not data.get("data"):
            data["data"] = {}

        return data


@app.get("/search/by-lastname",  tags=["Поиск"])
async def api_search_by_lastname(
    last_name: str = Query(..., description="Фамилия для поиска"),
    page: int = Query(0)
):
  
    try:
        result = await search_by_last_name(last_name, page)
        return result
    except Exception as e:
        raise HTTPException(status_code=500)

@app.get("/search/by-iin", response_model=SearchResponse, tags=["Поиск"])
async def api_search_by_iin(
    iin: str = Query(..., description="ИИН для поиска"),
    page: int = Query(0)
):
   
    try:
        result = await search_by_iin(iin, page)
        return result
    except Exception as e:
        raise HTTPException(status_code=500)



if __name__ == "__main__":
    import uvicorn
    import warnings
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    uvicorn.run(app, host="0.0.0.0", port=8000)