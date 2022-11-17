from controllers.routes.dashboard.atri import Atri
import os
import pandas as pd
from collections import defaultdict
import json


def get_data(file_name):
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', file_name)
    json_file = open(file_path)
    data = json.load(json_file)
    return data


def get_activity(filtered_data):
    fin_dic = []
    for i, j in filtered_data.items():
        j['x'] = i
        fin_dic.append({a: b for a, b in j.items() if a != 'FCEs_With_Procedure'})

    return fin_dic


def get_appointments(filtered_data):
    app_dict=[]
    months = ['31JUL22', '31AUG22', '30SEP22']
    for month in months:
        canceled_app = filtered_data[month]["Total_Appointments"] - filtered_data[month]["Attended_Appointments"] - filtered_data[month]["DNA_Appointments"]
        data_dict = {"x": month, 
                    "Attended_Appointments": filtered_data[month]["Attended_Appointments"],
                    "DNA_Appointments": filtered_data[month]["DNA_Appointments"],
                    "Canceled_Appointments": canceled_app
                    }
        app_dict.append(data_dict)
    return app_dict


def get_procedures(filtered_data):
    prep_data = {'FCE': 0, 'FCEs_With_Procedure': 0}
    for i, j in filtered_data.items():
        if i in get_specific_date_keys(21, ['JUL', 'AUG', 'SEP']):
            for k in prep_data.keys():
                prep_data[k] += filtered_data[i][k]
    prep_data['FCE_without_procedure'] = (prep_data['FCE'] - prep_data['FCEs_With_Procedure'])/prep_data['FCE']
    prep_data['FCEs_With_Procedure'] = prep_data['FCEs_With_Procedure'] / prep_data['FCE']
    prep_data.pop('FCE')
    data = [
        [{"name": i, "value": j} for i, j in prep_data.items()]
    ]
    return data


def get_ttm_activity(filtered_data):
    cols = [
            {"field": "id", "headerName": "Activity", "width":250},
            {"field": "start_date", "headerName": "Oct 2020 - Sep 2021", "width":200},
            {"field": "end_date", "headerName": "Oct 2021 - Sep 2022", "width":200},
            {"field": "percentage_change", "headerName": "% Change"}
            ]

    prep_data_1 = {'FCE':0, 'FCEs_With_Procedure':0, 'Ordinary_Admission_Episodes':0, 'FCE_DAY_CASES':0, 'FAE':0, 'EMERGENCY':0}
    for i,j in filtered_data.items():
        if i in get_specific_date_keys(20, ['OCT', 'NOV', 'DEC']) + get_specific_date_keys(21, ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP']):
            for k in prep_data_1.keys():
                prep_data_1[k] += filtered_data[i][k]

    prep_data_2 = {'FCE': 0, 'FCEs_With_Procedure': 0, 'Ordinary_Admission_Episodes': 0, 'FCE_DAY_CASES': 0, 'FAE': 0,
                   'EMERGENCY': 0}
    for i, j in filtered_data.items():
        if i in get_specific_date_keys(21, ['OCT', 'NOV', 'DEC']) + get_specific_date_keys(22, ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP']):
            for k in prep_data_2.keys():
                prep_data_2[k] += filtered_data[i][k]

    rows = [{"id": i, "start_date":prep_data_1[i], "end_date": prep_data_2[i], "percentage_change":(prep_data_2[i]-prep_data_1[i])*100/prep_data_1[i]} for i in prep_data_1.keys()]
    
    return cols, rows

def get_ytd_activity(filtered_data):
    cols = [
        {"field": "id", "headerName": "Activity"},
        {"field": "start_date", "headerName": "Apr 2021 - Sep 2021"},
        {"field": "end_date", "headerName": "Apr 2021 - Sep 2022"},
        {"field": "percentage_change", "headerName": "% Change"}
    ]

    prep_data_1 = {'FCE': 0, 'Ordinary_Admission_Episodes': 0, 'FCE_DAY_CASES': 0, 'FAE': 0,
                   'EMERGENCY': 0}
    for i, j in filtered_data.items():
        if i in get_specific_date_keys(21, ['APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP']):
            for k in prep_data_1.keys():

                prep_data_1[k] += filtered_data[i][k]

    prep_data_2 = {'FCE': 0, 'Ordinary_Admission_Episodes': 0, 'FCE_DAY_CASES': 0, 'FAE': 0,
                   'EMERGENCY': 0}
    for i, j in filtered_data.items():
        if i in get_specific_date_keys(22, ['APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP']):
            for k in prep_data_2.keys():
                prep_data_2[k] += filtered_data[i][k]

    rows = [{"id": i, "start_date": prep_data_1[i], "end_date": prep_data_2[i],
                                    "percentage_change": (prep_data_2[i] - prep_data_1[i]) * 100 / prep_data_1[i]} for i
                                   in prep_data_1.keys()]
    return cols, rows


# Helper


MONTH_DATE = {'JAN': 31,
              'FEB': 28,
              'MAR': 31,
              'APR': 30,
              'MAY': 31,
              'JUN': 30,
              'JUL': 31,
              'AUG': 31,
              'SEP': 30,
              'OCT': 31,
              'NOV': 30,
              'DEC': 31}


def get_specific_date_keys(year, months):
    keys = []
    for i in months:
        if i == 'FEB' and year%4 == 0:
            keys.append(str(29) + i + str(year))
        else:
            keys.append(str(MONTH_DATE[i]) + i + str(year))
    return keys


def internal_processing(data: pd.DataFrame):
    dic = defaultdict(dict)
    for i in data.values:
        dic_inter = {'FCE': i[3],
                       'FCEs_With_Procedure': i[4],
                       'Ordinary_Admission_Episodes':i[5],
                       'FCE_DAY_CASES': i[6],
                       'FAE': i[7],
                       'EMERGENCY': i[8]
                       }
        dic[str(i[1]) + ' ' + i[2].lower()][i[0]] = dic_inter
    with open("data/data.json", "w") as outfile:
        json.dump(dic, outfile, indent=4)

    print(dic)


def make_appointments_data():
    data = pd.read_csv('data/HES_M06_OPEN_DATA_TREATMENT_SPECIALTY.csv')
    sel_data = data[['Month_Ending', 'TRETSPEF', 'TRETSPEF_DESCRIPTION','Total_Appointments', 'Attended_Appointments', 'DNA_Appointments']]
    dic = defaultdict(dict)
    for i in sel_data.values:
        dic_inter = {'Total_Appointments': i[3],
                       'Attended_Appointments': i[4],
                       'DNA_Appointments':i[5],
                       }
        dic[str(i[1]) + ' ' + i[2].lower()][i[0]] = dic_inter
    with open("data/app_data.json", "w") as outfile:
        json.dump(dic, outfile, indent=4)

