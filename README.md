Validator Fields

<!-- ---------------------------------------------------------------------------------------------------------------------------- -->
📌 Objetivo

Este proyecto implementa un pipeline de validación de datos de enrollments de seguros médicos para un broker que opera con múltiples carriers y un marketplace externo.

El objetivo NO es comparar CSVs entre sí.
El objetivo es:
Detectar inconsistencias reales que generan pérdidas operativas, cancelaciones, errores de facturación y problemas de soporte.

<!-- ---------------------------------------------------------------------------------------------------------------------------- -->
validator_fields/
│
├── src/
│   ├── io/
│   │   ├── load_csv.py          # Solo lectura
│   │   └── save_reports.py
│   │
│   ├── cleaning/
│   │   ├── sherpa_cleaner.py
│   │   ├── crm_cleaner.py
│   │   └── common.py
│   │
│   ├── compare/
│   │   ├── matcher.py           # Cómo se cruzan los registros
│   │   ├── diff_engine.py       # Detecta diferencias
│   │   └── rules.py             # Qué se considera inconsistencia
│   │
│   ├── models.py                # Modelo mínimo común
│   │
│   └── pipeline.py              # Orquesta todo
│
├── data/
│   ├── raw/
│   │   ├── sherpa.csv
│   │   └── crm.csv
│   └── output/
│       └── inconsistencies.xlsx
│
├── tests/
│
├── requirements.txt
└── README.md