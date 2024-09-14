# Corutinas asincronas
Se tratan de funciones que nos permiten pausarlas y resumirlas durante la ejecución. Son especialmente utiles para manejar conexiones de red.

En este caso lo utilizaremos para llamar a una API de imagenes multiples veces con la ayuda de la libreria aiohttp, convertir los datos binarios obtenidos con la llamada a la API a un dato stream usando BytesIO y este archio convertirlo a un objeto Image usando PIL y finalmente mostrarl las imagenes en pantalla usando Tkinter y PIL.

## asyncio
Se trata de una biblioteca de python que nos permite manejar corutinas asincronas

## Funciones utilizadas
### `Fetch_image()`
>Nos permite obtener una imagen desde una URL
```
async def fetch_image(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            img_data = await response.read() 
            return Image.open(BytesIO(img_data))
        return None
```
>Si la respuesta de la llamada a la API resulta positiva, es decir con un codigo de estado 200 guardamos la imagen de forma binaria usando la función `read()`

>`session` se trata de un objeto que proviene de aiohttp.ClientSession()

```
async with session.get(url) as response:
        if response.status == 200:
            img_data = await response.read()
```
>`Image.open()` convierte un archivo a un objeto Image

>El archivo se obtiene con la función `BytesIO()` que transforma los datos binarios obtenidos en al petición a la API en un archivo
```
return Image.open(BytesIO(img_data))
```
---
### `Fetch_all_images()`
```
async def fetch_all_images():
    async with aiohttp.ClientSession() as session:
        coroutines = [fetch_image(session, url) for url in image_URLS] 
        images = await asyncio.gather(*coroutines)
        return images
```

> Se trata de una compresión de listas que contine objetos `Image` que fueron obtenidos a partir de una llamada a la API de imagenes usando la función `fetch_image()` y la lista de URLs de la API de imagenes

>En resumen por cada URL en la lista `image_URLS`, se agrega a la lista `coroutines` el objeto Image resultante.
```
coroutines = [fetch_image(session, url) for url in image_URLS]
```
>`asyncio.gather()` espera a que las corutinas terminen y devuelve el resultado de cada una de ellas en una lista
```
images = await asyncio.gather(*coroutines)
```
---
### `main()`
> `asyncio.run()` ejecuta la corutina (función asíncrona) `fetch_all_images()` en un entorno síncrono
```
def main() -> None:
    images = asyncio.run(fetch_all_images())
```
