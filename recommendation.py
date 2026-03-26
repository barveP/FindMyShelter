import pandas as pd
import joblib
import json

# Load Long Beach model and columns
lb_model = joblib.load('longbeach_best_model.pkl')
with open('longbeach_columns.json', 'r') as f:
    lb_columns = json.load(f)

# Load San Jose model and columns
sj_model = joblib.load('sanjose_best_model.pkl')
with open('sanjose_columns.json', 'r') as f:
    sj_columns = json.load(f)

# Austin - uncomment when files are ready
# austin_model = joblib.load('austin_best_model.pkl')
# with open('austin_columns.json', 'r') as f:
#     austin_columns = json.load(f)


def recommend_shelter(animal_type, primary_color, sex, age_days, intake_condition):

    # Create input dataframe
    input_df = pd.DataFrame([{
        'AnimalType': animal_type,
        'PrimaryColor': primary_color,
        'Sex': sex,
        'Age': age_days,
        'IntakeCondition': intake_condition
    }])

    # One-hot encode
    input_encoded = pd.get_dummies(input_df)

    # Long Beach prediction
    lb_input = input_encoded.reindex(columns=lb_columns, fill_value=0)
    lb_prob = lb_model.predict_proba(lb_input)[0][1]

    # San Jose prediction
    sj_input = input_encoded.reindex(columns=sj_columns, fill_value=0)
    sj_prob = sj_model.predict_proba(sj_input)[0][1]

    # Austin prediction - uncomment when ready
    # austin_input = input_encoded.reindex(columns=austin_columns, fill_value=0)
    # austin_prob = austin_model.predict_proba(austin_input)[0][1]

    results = {
        'Long Beach': round(lb_prob * 100, 1),
        'San Jose': round(sj_prob * 100, 1),
        # 'Austin': round(austin_prob * 100, 1)
    }

    best_shelter = max(results, key=results.get)

    return results, best_shelter


# Test
if __name__ == '__main__':
    test_cases = [
        ('dog', 'brown', 'neutered', 365, 'normal'),
        ('cat', 'black', 'spayed', 730, 'ill'),
        ('other', 'white', 'male', 180, 'injured'),
    ]

    for animal_type, color, sex, age, condition in test_cases:
        results, best = recommend_shelter(animal_type, color, sex, age, condition)
        print(f'\nInput: {animal_type}, {color}, {sex}, {age} days, {condition}')
        print(f'Results: {results}')
        print(f'Recommended shelter: {best}')