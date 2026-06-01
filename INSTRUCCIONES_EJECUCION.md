# Instrucciones de ejecución

## 1. Ubicación recomendada

Descomprimir la carpeta `proyecto_churn_mlops` dentro de:

```text
C:\Users\Marcelo\mlops_pruebas
```

La estructura esperada será:

```text
C:\Users\Marcelo\mlops_pruebas\proyecto_churn_mlops
```

## 2. Abrir el proyecto en VS Code

En Visual Studio Code:

```text
Archivo > Abrir carpeta
```

Seleccionar:

```text
C:\Users\Marcelo\mlops_pruebas
```

## 3. Activar el entorno virtual

Desde la terminal de VS Code, ubicada en:

```powershell
C:\Users\Marcelo\mlops_pruebas
```

ejecutar:

```powershell
.\.venv\Scripts\Activate.ps1
```

Debe aparecer:

```powershell
(.venv) PS C:\Users\Marcelo\mlops_pruebas>
```

## 4. Entrar al proyecto

```powershell
cd proyecto_churn_mlops
```

## 5. Instalar librerías

```powershell
python -m pip install -r requirements.txt
```

## 6. Ejecutar preparación de datos

```powershell
python src\preparar_datos.py
```

## 7. Entrenar el modelo

```powershell
python src\entrenar_modelo.py
```

## 8. Evaluar el modelo

```powershell
python src\evaluar_modelo.py
```

## 9. Ejecutar la API

```powershell
uvicorn api.main:app --reload
```

Abrir en el navegador:

```text
http://127.0.0.1:8000
```

Documentación automática:

```text
http://127.0.0.1:8000/docs
```

## 10. Probar la API

En Swagger, usar el endpoint:

```text
POST /predict
```

Ejemplo de entrada:

```json
{
  "edad": 28,
  "antiguedad_meses": 8,
  "saldo_promedio": 1200,
  "reclamos": 3,
  "usa_app": 0
}
```

## 11. Ejecutar pruebas

Detener la API con `Ctrl + C` y ejecutar:

```powershell
pytest
```

Resultado esperado:

```text
2 passed
```
## Nota sobre trazabilidad

Cada cambio importante del proyecto debe registrarse mediante commits claros y descriptivos.

Esto permite conocer la evolución del código, la documentación, las pruebas y la configuración del proyecto.
