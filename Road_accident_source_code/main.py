import pandas as pd
import configuration  # importing values from configuration file
from accident_database import mysql_data

feature = []
suggestion = []

def execution(feature_keys):
    for data in feature_keys:
        data = int(data)
        if data in configuration.feature_dict.keys():
            feature.append(configuration.feature_dict[data]) # Separating feature name to use in SQL query based on key
        elif data in configuration.state_dict.keys():
            state_name = configuration.state_dict[data] # Separating state name to use in SQL query based on key
    fetch_data = mysql_data(state_name, feature) # calling MYSQL to execute the query
    actual_value = pd.Series(fetch_data[0]) # Contains values for each feature
    threshold_value = pd.Series(fetch_data[1]) # Contains threshold values for each feature
    difference_value = threshold_value.astype('float') - actual_value.astype('float')  # Variance from the threshold
    # Formula based on the weightage
    # 50% value for difference value lesser than -5
    # 25% value for difference value between -3 and -5
    # 10% value for difference value between 0 and -3
    # 8% value for difference value between 0 and 3
    # 5% value for difference value between 3 and 5
    # 2% value for difference value greater than 5

    accident_threshold_value = difference_value.apply(
        lambda x: x * 5 / 100 if (3.0 < x < 5.0) else (x * 8 / 100 if (0 < x < 3.0) else (
            x * 10 / 100 if (-3 < x < 0) else (
                x * 25 / 100 if (-5 < x < -3) else (x * 50 / 100 if (x < -5) else x * 2 / 100)))))
    for data in feature:
        if data in configuration.user_suggestion.keys():
            suggestion.append(configuration.user_suggestion[data]) # Appending suggestion data to publish in webpage
    overall_safety = accident_threshold_value.sum() # Overall safety status of the travel
    # accident_threshold_dict = dict(zip(suggestion, accident_threshold_value))
    return suggestion, accident_threshold_value, overall_safety

