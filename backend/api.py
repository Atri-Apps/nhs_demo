from controllers.routes.dashboard.atri import Atri
import os
import pandas as pd
from collections import defaultdict
import json


def apply_dropdown_values(at: Atri):
    json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'data.json')
    json_file = open(json_file_path)
    data = json.load(json_file)
    at.Dropdown1.custom.values = list(data.keys())
    at.Dropdown1.custom.selectedValue = '100 general surgery service'
    set_filter(at, '100 general surgery service')


def set_filter(at: Atri, selected_filter: str):
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'data.json')
    json_file = open(file_path)
    data = json.load(json_file)
    set_line_chart_data(at, data[selected_filter])
    set_appointments(at, selected_filter)
    set_year_to_data_comparison_data(at, data[selected_filter])
    set_rolling_12_month_data(at, data[selected_filter])
    get_fc_with_procedures(at, data[selected_filter])
    pass


def set_line_chart_data(at: Atri, filtered_data):
    fin_dic = []
    for i, j in filtered_data.items():
        j['x'] = i
        fin_dic.append({a: b for a, b in j.items() if a != 'FCEs_With_Procedure'})

    at.admissions.custom.data = fin_dic
    pass


def set_rolling_12_month_data(at: Atri, filtered_data):
    at.ttm_episodes.custom.cols = [
                                    {"field": "id", "headerName": "Activity"},
                                    {"field": "start_date", "headerName": "Oct 2020 - Sep 2021"},
                                    {"field": "end_date", "headerName": "Oct 2021 - Sep 2022"},
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

    at.ttm_episodes.custom.rows = [{"id": i, "start_date":prep_data_1[i], "end_date": prep_data_2[i], "percentage_change":(prep_data_2[i]-prep_data_1[i])*100/prep_data_1[i]} for i in prep_data_1.keys()]
    pass


def set_year_to_data_comparison_data(at: Atri,filtered_data):
    at.ytd_episodes.custom.cols = [
        {"field": "id", "headerName": "Year to date comparison"},
        {"field": "start_date", "headerName": "April 2021-Sep 2021"},
        {"field": "end_date", "headerName": "April 2021 - Sep 2022"},
        {"field": "percentage_change", "headerName": "Age", "type": "% Change"}
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

    at.ytd_episodes.custom.rows = [{"id": i, "start_date": prep_data_1[i], "end_date": prep_data_2[i],
                                    "percentage_change": (prep_data_2[i] - prep_data_1[i]) * 100 / prep_data_1[i]} for i
                                   in prep_data_1.keys()]
    pass


def get_fc_with_procedures(at: Atri, filtered_data):
    prep_data = {'FCE': 0, 'FCEs_With_Procedure': 0}
    for i, j in filtered_data.items():
        if i in get_specific_date_keys(21, ['JUL', 'AUG', 'SEP']):
            for k in prep_data.keys():
                prep_data[k] += filtered_data[i][k]
    prep_data['FCE_without_procedure'] = (prep_data['FCE'] - prep_data['FCEs_With_Procedure'])/prep_data['FCE']
    prep_data['FCEs_With_Procedure'] = prep_data['FCEs_With_Procedure'] / prep_data['FCE']
    prep_data.pop('FCE')
    at.procedures.custom.data = [
        [{"name": i, "value": j} for i, j in prep_data.items()]
    ]
    at.procedures.custom.options = [
        # options for first circle
        {
            "cx": "50%",  # center of the circle's x
            "cy": "50%",  # center of the circle's y
            "showLabel": True,
            "animate": False,
        }
    ]
    at.procedures.custom.toolTip = {"show": True}
    at.procedures.custom.legend = {"show": True}


def set_appointments(at: Atri, selected_filter: str):
    json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'app_data.json')
    json_file = open(json_file_path)
    data = json.load(json_file)
    filtered_data = data[selected_filter]
    prep_data_1 = {'Total_Appointments': 0, 'Attended_Appointments': 0, 'DNA_Appointments': 0}
    for i, j in filtered_data.items():
        if i in get_specific_date_keys(22, ['JUL']):
            for k in prep_data_1.keys():
                prep_data_1[k] += filtered_data[i][k]
    prep_data_1['x'] = '31JUL22'
    prep_data_2 = {'Total_Appointments': 0, 'Attended_Appointments': 0, 'DNA_Appointments': 0}
    for i, j in filtered_data.items():
        if i in get_specific_date_keys(22, ['AUG']):
            for k in prep_data_2.keys():
                prep_data_2[k] += filtered_data[i][k]
    prep_data_2['x'] = '31AUG22'
    prep_data_3 = {'Total_Appointments': 0, 'Attended_Appointments': 0, 'DNA_Appointments': 0}
    for i, j in filtered_data.items():
        if i in get_specific_date_keys(22, ['SEP']):
            for k in prep_data_3.keys():
                prep_data_3[k] += filtered_data[i][k]
    prep_data_3['x'] = '31SEP22'
    fin_dic = [prep_data_1, prep_data_2, prep_data_3]
    at.appointments.custom.data = fin_dic
    pass


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

