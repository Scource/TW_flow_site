from django.core.files.base import ContentFile

from io import BytesIO
import pandas as pd
from datetime import datetime

from .models import Report, ReportItem
from .scripts import choose_from

reports_name_dict={
    'dbs_peak_values':'Dane zawyzone i zera',
    'dbs_statuses': 'Raport statusow',
    'dbs_check_node': 'Raport wezlow',
    'dbs_check_conf': 'Raport konfiguracji i zatweerdzania',
    'dbs_get_PPE': 'Zestawienie PPE',
    'dbs_check_MB_PPE': 'Porownanie MBvsPPE',
}

def create_report(user, url, **kwargs):
    main_rap = Report(base_number=1, report_author=user,
                      report_type=set_report_type(url))
    main_rap.save()


    
    if url == 'dbs_get_PPE':
        for pob in kwargs['POB_elements']:
            if (pob.cspr_id is not None):
                create_report_item(main_rap, url, kwargs, pob)
    else:
        create_report_item(main_rap, url, kwargs)

    main_rap.end = datetime.now()
    main_rap.save()
    return main_rap.id

def set_report_name(url, kwargs, pob=None):
    if 'date_to' in kwargs:
        date_to_str = f"_{kwargs.get('date_to')}"
    else:
        date_to_str=""
    if pob:
        pob_str = f'_{pob.code}'
    else:
        pob_str=""
    return f"{reports_name_dict.get(url)}{pob_str}_{kwargs.get('date_from')}{date_to_str}.xlsx"

def set_report_type(url):
    return f"{reports_name_dict.get(url)}"


def create_report_item(main_rap, url, kwargs, pob=None):

    in_memory_fp = BytesIO()
    doc = ReportItem(
        report=main_rap, report_name=set_report_name(url, kwargs, pob))
    function = choose_from(url, 2)
    data = function(kwargs, pob) 
    
    #df.to_excel(pd.ExcelWriter(in_memory_fp, engine='xlsxwriter'))
    writer = pd.ExcelWriter(in_memory_fp, engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Raport')
    writer.save()


    xlsx_data = ContentFile(in_memory_fp.getvalue())
    doc.report_file.save(doc.report_name, xlsx_data)
    doc.end = datetime.now()
    doc.save()
