# SpaceGuard Insurance Dashboard

## Projektbeschreibung
SpaceGuard ist eine Plattform für Risikoversicherung im Bereich Weltraumrisiken.  
Das System nutzt NASA-Daten zu Near-Earth Objects (NEOs), um das finanzielle Risiko von Asteroideneinschlägen automatisiert zu bewerten.

## Kernfunktionen

- ETL-Pipeline: Automatisierte Extraktion und Bereinigung von NASA-Datensätzen  
- Risk Engine: Berechnung von kinetischer Energie (Terajoule) und Impuls und daraus resultierendem Risk Score 
- Dynamic Pricing:  Prämienberechnung basierend auf Zerstörungskraft und Eintrittswahrscheinlichkeit  
- Ausschluss von als „Hazardous“ klassifizierten Objekten  

---

## 🛠 Tech-Stack

- **Python 3.x**
- **Streamlit**
- **Pandas & NumPy**
- **SQLite**

---

## Installation & Ausführung

```bash
git clone https://github.com/ayoub63/spacial-insurance.git
cd spacial-insurance
pip install -r requirements.txt
python etl.py
streamlit run frontend/Home.py