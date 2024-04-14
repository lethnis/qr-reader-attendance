# Сканер QR-кодов с изображений и видео  
<table>
  <tr>
    <td><img src=data/corona.jpg width=400></td>
    <td><img src=output/corona.jpg width=400></td>
  </tr>
  <tr>
    <td><img src=data/link.jpg width=400></td>
    <td><img src=output/link.jpg width=400></td>
  </tr>
  <tr>
    <td><img src=data/message.jpg width=400></td>
    <td><img src=output/message.jpg width=400></td>
  </tr>
</table>

# Использование
Добавить видео и изображения в папку *data/* и запустить `python main.py`

# Система доступа по камере
В файле *whitelist.txt* содержится список разрешённых пользователей. В файле *log.txt*
содержатся записи о предоставлении доступа с именем и датой. Запустить можно командой
`python webcam_access.py`

# Пример системы доступа по камере
https://github.com/lethnis/qr-reader-attendance/assets/88483002/f1fcd928-3b00-4c27-899a-615ed99deae6
