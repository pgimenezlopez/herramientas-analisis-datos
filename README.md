# ⚙️ PGL Centro de Soluciones

**Plataforma centralizada de Ingeniería de Datos y Automatización de Procesos.**
Este repositorio aloja una suite de herramientas desarrolladas en Python para resolver ineficiencias operativas en logística, finanzas y gestión de clientes.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Estado-En_Desarrollo-green)

## 🚀 Módulos del Sistema

La aplicación actúa como un "Hub Central" que orquesta cuatro soluciones independientes:

### 1. 📊 Monitor STM (Business Intelligence)
Dashboard analítico para la visualización de datos de transporte público.
- **Stack:** Pandas, Plotly.
- **Función:** Mapeo de paradas y detección de patrones de movilidad urbana.

### 2. 📂 Consolidador Excel (ETL Automation)
Motor de procesamiento para unificar reportes dispersos.
- **Problema:** Procesos manuales de copy-paste en departamentos administrativos.
- **Solución:** Script que fusiona múltiples archivos `.xlsx` o `.csv` en un reporte maestro estandarizado en segundos.

### 3. 🐾 Gestión Veterinaria (CRM)
Sistema de retención de clientes basado en alertas preventivas.
- **Función:** Cálculo automático de fechas de vencimiento de vacunas y generación de listas de contacto para recordatorios.

### 4. 🧘 Plataforma de Coaching (Seguimiento)
Herramienta de gestión para profesionales de la salud/coaching.
- **Función:** Registro de evolución de pacientes, historial de sesiones y métricas de progreso personal.

---

## 🛠️ Instalación y Uso Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/pgimenezlopez/herramientas-analisis-datos.git](https://github.com/pgimenezlopez/herramientas-analisis-datos.git)

2. **Instalar dependiencias:**
pip install -r requirements.txt

3. **Ejecutar la suite:**
streamlit run Home.py