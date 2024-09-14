import tkinter as tk
import asyncio
import aiohttp
from PIL import Image, ImageTk
from io import BytesIO

image_URLS = [
    "https://picsum.photos/200/300",
    "https://picsum.photos/300/200",
    "https://picsum.photos/250/250"
]

async def fetch_image(session: aiohttp.ClientSession, url: str) -> Image:
    # with se encarga de gestionar el ciclo de vida de los recursos, abrir y cerrar la conexión
    async with session.get(url) as response:
        if response.status == 200:
            # response.read lee el contenido en bruto de la imagen
            img_data = await response.read()
            # BytesIO Simula un archivo en memoria. Convierte datos binarios en en un "archivo"
            # BytesIO(img_data()) es un stream de bytes que contiene la imagen
            # Image toma un archivo (imagen) y lo convierte en un objeto Image para que tkinter lo pueda interpretar 
            return Image.open(BytesIO(img_data))
        return None

async def fetch_all_images() -> list:
    async with aiohttp.ClientSession() as session:
        coroutines = [fetch_image(session, url) for url in image_URLS]
        # * es para cuando usamos listas, similar a .gather(coroutines[0], coroutines[1], ...) 
        images = await asyncio.gather(*coroutines)
        return images

def interface(images: list) -> None:
    root = tk.Tk()
    root.title("Asyncio")
    
    for i, img in enumerate(images):
        img_tk = ImageTk.PhotoImage(img)
        lb = tk.Label(root, image=img_tk)
        lb.image = img_tk
        lb.grid(row=i, column=0)
        
    root.mainloop()

def main() -> None:
    # Logica de fetch de imagenes
    images = asyncio.run(fetch_all_images())
    # Mostar imagenes
    interface(images)

main()