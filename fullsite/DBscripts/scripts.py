import time
import pandas as pd
from .models import *
from .forms import GetPeakValuesForm, GetStandardDataForm

PEAK_VALUES_DESC = "Pobieranie z bazy PPE, dla których w danych 15' wolumen jest wyższy niż podana wartość"
DATA_STATUSES_DESC = 'Pobieranie z bazy PPE dla których wsytępują braki, prognozy lub dane niepewne'
CHECK_NODE_DESC = 'Pobieranie z bazy PPE, dla których istnieje konf. handlowa i brak węzła'
CHECK_CONF_DESC = 'Pobieranie z bazy PPE, dla których istnieje konf. handlowa i brak danych zatwierdzonych (N/A)'
GET_PPE_DESC = 'Pobieranie z bazy zestawienia PPE dla wskazanego MB'
CHECK_MB_PPE_DEC = 'Tworzy porównanie danych agregatu MB z listą jego PPE'

def choose_from(url, return_type):
    if url == 'dbs_peak_values':
        if return_type==1:
            return GetPeakValuesForm
        elif return_type==2:
            return get_peak_values
        else:
            return PEAK_VALUES_DESC
    elif url == 'dbs_statuses':
        if return_type == 1:
            return GetStandardDataForm
        elif return_type==2:
            return get_data_statuses
        else:
            return DATA_STATUSES_DESC
    elif url == 'dbs_check_node':
        if return_type == 1:
            return GetStandardDataForm
        elif return_type == 2:
            return get_nodes
        else:
            return CHECK_NODE_DESC
    elif url == 'dbs_check_conf':
        if return_type == 1:
            return GetStandardDataForm
        elif return_type == 2:
            return get_configuration_problems
        else:
            return CHECK_CONF_DESC
    elif url == 'dbs_get_PPE':
        if return_type == 1:
            return GetStandardDataForm
        elif return_type == 2:
            return get_PPE_list
        else:
            return GET_PPE_DESC
    elif url == 'dbs_check_MB_PPE':
        if return_type == 1:
            return GetStandardDataForm
        elif return_type == 2:
            return check_MB_PPE
        else:
            return CHECK_MB_PPE_DEC


def get_peak_values(data, pob):
    df=pd.DataFrame(columns=['a', 'b'])
    for p in range(1, data['value']):
        time.sleep(1)
        print(p)
    return df


def get_data_statuses(data, pob):
    df = pd.DataFrame(columns=['a', 'b'])
    print(data['login'])
    print(data['password'])
    print(data['date_from'])
    print(data['date_to'])
    assas = list(data['POB_elements'].values_list('cspr_id', flat=True))
    assas.remove(None)
    assas=tuple(assas)

    return df


def get_nodes(data, pob):
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)
    for p in (data):
        time.sleep(1)
        print(p)
    return df


def get_configuration_problems(data, pob):
    df = pd.DataFrame(columns=['a', 'b'])
    for p in range(1, data['value']):
        time.sleep(1)
        print(p)
    return df


def get_PPE_list(data, pob):
    print(pob.cspr_id)
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)
    time.sleep(10)
    print(df)
    return df


def check_MB_PPE(data, pob):
    df = pd.DataFrame(columns=['a', 'b'])
    for p in range(1, data['value']):
        time.sleep(1)
        print(p)
    return df

