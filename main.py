from fastapi import FastAPI, HTTPException, Response
import undetected_chromedriver as uc
import time

# Простой веб-сервер с одним GET запросом /get_html?url=https://ozon.ru/...
app = FastAPI()

@app.get("/get_html")
async def scrape_page(url: str, scroll_times: int = 3, scroll_delay: float = 2):
    try:
        # Запуск браузера в стандартном оконном режиме
        options = uc.ChromeOptions()
        options.headless = False
        
        driver = uc.Chrome(options=options)

        # Открытие сайта
        driver.get(url)
        time.sleep(3)
        
        # Скроллинг вниз для прогрузки некоторой части контента
        for _ in range(scroll_times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_delay)

        # Исходник страницы
        html = driver.page_source
        driver.quit()

        # Возвращаем чистый HTML чтобы его уже спарсить
        return Response(content=html, media_type="text/plain")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
