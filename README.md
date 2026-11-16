# Pet Adoption Shelter Finder

A data-driven recommendation system that helps you find the best shelter for a lost or stray pet based on its characteristics and historical adoption data.

## How It Works

Enter a pet's details and the system runs them through machine learning models trained on real shelter data from Long Beach, San Jose, and Austin. It returns the adoption probability for each shelter and recommends the one with the highest chance of adoption.

## Shelters Included

- Long Beach Animal Shelter (Long Beach, CA)
- San Jose Animal Services (San Jose, CA)
- Austin Animal Center (Austin, TX)

## Project Structure
```
PET-ADOPTION-RECOMMENDER/
├── app.py                 
├── recommendation.py         
├── longbeach_best_model.pkl  
├── longbeach_columns.json    
├── sanjose_best_model.pkl    
├── sanjose_columns.json      
└── requirements.txt          
```

## How To Run

**Step 1: Clone the repository**
```bash
git clone "repository address"
cd pet-adoption-recommender
```

**Step 2: Create a virtual environment**
```bash
python3 -m venv venv
```

**Step 3: Activate the virtual environment**
```bash
source venv/bin/activate
```

**Step 4: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 5: Run the app**
```bash
streamlit run app.py
```

**Step 6: Open in browser**
```
http://localhost:8501
```

## Input Fields

| Field | Options |
|-------|---------|
| Animal Type | dog, cat, other |
| Primary Color | black, brown, white, gray, orange, tan, multicolor, other |
| Sex | neutered, spayed, male, female, unknown |
| Intake Condition | normal, ill, injured, behavior, other |
| Age | Number of days |

## Models

All models are Random Forest classifiers trained with 5-fold stratified cross validation.

| Shelter | AUC | Accuracy | F1 |
|---------|-----|----------|----|
| Long Beach | 0.82 | 78.9% | 0.61 |
| San Jose | 0.89 | 82.9% | 0.81 |

## Team

CS7180 - Practical AI