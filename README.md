# Validator Fields

## 📌 Purpose

This project implements a structured data validation pipeline for health insurance enrollments handled by a broker operating across multiple carriers and an external marketplace.

The goal is **not** to compare CSV files blindly.  
The goal is to detect **real operational inconsistencies** that cause:

- Policy cancellations  
- Billing discrepancies  
- Revenue leakage  
- Carrier reporting errors  
- Customer support escalations  

This repository focuses on identifying financially and operationally critical data mismatches before they impact the business.

---

## 🏗 Architecture Overview
Raw Data (CRM / Marketplace)
↓
Load
↓
Clean & Normalize
↓
Match Records
↓
Detect Differences
↓
Apply Business Rules
↓
Generate Inconsistency Repor


Each layer has a single responsibility and is isolated for maintainability and testability.

---

## 📂 Project Structure
validator_fields/
│
├── src/
│ ├── cleaning/
│ │ ├── sherpa_cleaner.py # Marketplace normalization
│ │ ├── crm_cleaner.py # CRM normalization
│ │ └── common.py # Shared transformations
│ │
│ ├── compare/
│ │ ├── matcher.py # Record matching logic
│ │ ├── diff_engine.py # Field-level difference detection
│ │ └── rules.py # Business inconsistency rules
│ │
│ ├── models.py # Canonical shared data model
│ │
│ └── pipeline.py # Orchestration layer
│
├── data/
│ ├── raw/
│ │ ├── sherpa.csv
│ │ └── crm.csv
│ └── output/
│ └── inconsistencies.xlsx
│
├── tests/
│
├── requirements.txt
└── README.md


---

## 🎯 Design Principles

- Single responsibility per module  
- Deterministic matching logic  
- Explicit business rules  
- Reproducible validation outputs  
- Clear separation between cleaning, comparison, and rule evaluation  

---

## 🔎 What This Project Solves

This validator identifies issues such as:

- Premium mismatches  
- Subsidy inconsistencies  
- Missing enrollments  
- Status discrepancies  
- Effective date conflicts  
- Identifier mismatches  

The output is a structured report designed for operational review and corrective action.

---

## 🧪 Testing

The `tests/` directory ensures that:

- Matching logic behaves deterministically  
- Transformation rules remain stable  
- Critical financial calculations are validated  

No business logic should be added without corresponding test coverage.