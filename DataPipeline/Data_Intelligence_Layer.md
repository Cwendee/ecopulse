# EcoPulse – Data Intelligence Layer Breakdown

## 1. Disclaimer
The platform **does not predict floods in real time** and does not coordinate emergency response.
Its purpose is to translate existing climate data into **simple, actionable preparedness guidance**.
Climate data already exists — our job is to make it understandable and usable.

## 2. Role of the Data Science Team
The Data Science team builds the platform’s **risk intelligence layer**, which is the **single source of truth** for flood‑related insights.
We convert:
**Climate / rainfall data → regional flood risk levels → structured outputs for the map, alerts, and ECO assistant**
Other teams build the UI, alerts, and AI explanations, but all risk information originates from our **pipeline**.

### Core Responsibilities
- Location preprocessing & mapping
- Flood risk classification logic
- Local emergency resources integration (verified + AI-augmented)
- Data validation, determinism & reproducibility
- Backend integration support

## 3. MVP Technical Approach
For the MVP, we use:
- **One public dataset**: CHIRPS Daily (Africa-wide via STAC API)
- **A rainfall‑based flood risk proxy**: 
  - `Risk_Score = Current_Rainfall (7-day window) / Historical_Mean_Rainfall (60-day window)`
- **Region‑level aggregation**: ADM2 polygons (geoBoundaries CGAZ)
- **Deterministic rule‑based classification**: 
  - Required by PRD: same input → same output
  - No machine learning for risk calculation
  - Fast, explainable, scalable logic

## 4. AI & Model Architecture
We leverage **OpenRouter** as the unified gateway for our AI capabilities.

### AI Model: GPT-4o-mini
- **Link**: [https://openrouter.ai/openai/gpt-4o-mini/api](https://openrouter.ai/openai/gpt-4o-mini/api)
- **Implementation**: GPT-4o-mini via OpenRouter.
- **Key Roles**:
  - **Location Resolver**: Interpreting messy user location strings (e.g., "Ajah, Lagos") and mapping them to stable ADM2 `region_id`s.
  - **ECO Assistant**: Generating natural-language explanations and practical preparedness advice based on technical risk metrics.
- **Constraint**: We **do not rely on GPT-4o-mini for numerical flood modeling**. All risk scores are calculated deterministically by the Data Science pipeline.

## 5. Location Intelligence
### 5.1 ADM2 Dataset
- Uses **geoBoundaries CGAZ ADM2**, filtered to Africa.
- Each region receives:
  - A stable `region_id` (shapeID)
  - A polygon boundary
  - Human-readable metadata: `country`, `region_name`, `country_code`

### 5.2 Mapping User Input → `region_id`
- **Deterministic mapping**: For clean inputs (dropdowns). Exact match against ADM2 names.
- **AI-Powered Resolver**: Uses `gpt-4o-mini` to select the best ADM2 region from a candidate list for unstructured user input.

## 6. Rainfall & Risk Engine
### 6.1 Data Source
- **CHIRPS Daily** rainfall from **Digital Earth Africa** via STAC API.
- Fully automated; updated every **24 hours**.

### 6.2 Risk Calculation
- Analyzes a **7-day rolling window** of rainfall.
- Compares it against a **60-day historical baseline**.
- **Deterministic output**: Same rainfall data always results in the same risk level.

## 7. Resource Intelligence (Local Resources Tab)
The platform provides a **Resource Intelligence Layer** to help users take action.

### 7.1 Emergency Contacts Dataset
- **Primary Source**: A curated dataset (CSV/Excel) containing official contacts.
- **Columns**: `ISO3`, `shapeID`, `Police`, `Fire`, `Ambulance`, `notes`.
- **Logic**: Matches user's `region_id` to the dataset to provide verified local help.

### 7.2 AI-Augmented Resources
- `gpt-4o-mini` finds localized community shelters and Red Cross chapters.
- **Figma Alignment**: Output is categorized into "Local Emergency Contacts" and "Local Shelters" to match the UI design.

## 8. Data Science Deliverables (Checklist)
- [x] Location normalization & AI Resolver logic.
- [x] Deterministic risk classification rules.
- [x] STAC API automated rainfall ingestion.
- [x] Verified resources dataset loader.
- [x] Metadata merging for backend readiness (`risk_africa.parquet`).
- [x] Fail-secure logic for missing data.
