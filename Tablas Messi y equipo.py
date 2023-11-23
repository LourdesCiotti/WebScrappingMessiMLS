import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configura el servicio de ChromeDriver (ajusta la ruta)
service = ChromeService(executable_path="C:/Users/Lufly/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
service.start()

# Configura el navegador Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ejecuta Chrome en modo sin cabeza (sin ventana)
driver = webdriver.Chrome(service=service, options=options)

# URL de la página a la que deseas hacer web scraping
url = "https://www.mlssoccer.com/stats/clubs/#season=2022&competition=mls-regular-season&statType=CLUB_STATS_GENERAL_POSTSEASON"

# Abre la URL con Selenium
driver.get(url)

# Espera a que la tabla se cargue en la página (ajusta el tiempo de espera según sea necesario)
wait = WebDriverWait(driver, 15)
stats_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.mls-o-table.club-stats')))

# Extraer encabezados de la tabla
# header_row = stats_table.find_element(By.TAG_NAME, "thead")
# header_columns = header_row.find_elements(By.TAG_NAME, "th")
# header_texts = [column.text for column in header_columns]

# Extraer encabezados de la tabla
header_row = stats_table.find_element(By.TAG_NAME, "thead")
header_columns = header_row.find_elements(By.TAG_NAME, "th")
header_texts = []
# Iterar a través de las columnas de encabezados y agregar los textos a la lista
for column in header_columns:
    header_texts.append(column.text)
# Eliminar el primer elemento vacío de la lista de encabezados
header_texts.pop(0)
print(header_texts)
# Inicializar una lista para almacenar los datos
data = []

# Ahora puedes procesar los datos de la tabla (excluyendo la fila de encabezados)
data_rows = stats_table.find_elements(By.CSS_SELECTOR, 'tbody tr')
for row in data_rows:
    # Extraer el nombre del club (primera columna)
    club_name = row.find_element(By.CSS_SELECTOR, 'span.mls-o-table__abbreviation').text
    
    # Extraer los valores de la tabla (segundas columnas en adelante)
    columns = row.find_elements(By.TAG_NAME, "td")[1:]
    row_data = [club_name] + [column.text for column in columns]
    
    # Agregar los datos de la fila a la lista
    data.append(row_data)

# Cierra el navegador y el servicio de ChromeDriver
driver.quit()
service.stop()

# Guardar los datos en un archivo CSV
csv_filename = "mls_data2022_ClubStats.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Escribir los encabezados
    csv_writer.writerow(header_texts)
    
    # Escribir los datos
    csv_writer.writerows(data)

print(f"Los datos se han guardado en '{csv_filename}'")
