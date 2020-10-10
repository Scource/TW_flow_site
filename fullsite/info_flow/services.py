from .models import tasks, process, comments, category
from django.db import models
import datetime
import calendar


def get_tasks_in_proc(pid):
	task=tasks.objects.all().filter(tasks_proc=pid, tasks_is_deleted=False)
	all_number=task.count()
	tasks_number=task.filter(tasks_tasks_id__isnull=True).count()
	points_number=task.filter(tasks_tasks_id__isnull=False).count()
	tasks_number_inactive=task.filter(tasks_tasks_id__isnull=True, tasks_is_active=False).count()
	points_number_active=task.filter(tasks_tasks_id__isnull=False, tasks_is_active=False).count()
	Dict = {'task':all_number, 'tasks_number':tasks_number , 'points_number':points_number, 
			'tasks_number_inactive':tasks_number_inactive, 'points_number_active':points_number_active}
	return Dict


def get_points_in_task(tid):
	task=tasks.objects.all().filter(tasks_tasks_id=tid, tasks_is_deleted=False)
	points_number=task.filter(tasks_tasks_id__isnull=False).count()
	points_number_inactive=task.filter(tasks_tasks_id__isnull=False, tasks_is_active=False).count()
	Dict = {'points_number':points_number, 'points_number_inactive':points_number_inactive}
	return Dict



def create_corrections_template(user, cor_data, cor):
	cor_data_end=cor_data.replace(day=calendar.monthrange(cor_data.year, cor_data.month)[1], hour=23, minute=59)


	tasks_names_list=['MB Odbiorcze  v1', 'MB Odbiorcze  v2', 'MB Wytwórcze  v1', 'MB Wytwórcze  v2', 'Weryfikacja Odbiorczego Oddania', 'Raport "KOREKTY_MB_MC"']
	tasks_desc_list=['Zadania związane z przygotowaniem danych w celu wysłania na Rynek Bilansujący MB odbiorczych',
	'Dodatkowa iteracja zadań związane z przygotowaniem danych w celu wysłania na Rynek Bilansujący MB odbiorczych',
	'Zadania związane z przygotowaniem danych w celu wysłania na Rynek Bilansujący MB wytwórczych',
	'Dodatkowa iteracja zadań związanych z przygotowaniem danych w celu wysłania na Rynek Bilansujący MB wytwórczych',
	'Sprawdzenie konfiguracji technicznej i handlowej dla wszystkich MBo na kierunku oddanie dla prosumentów/mikroinstalacji',
	'Po zakończeniu wcześniejszych prac związanych z weryfikacją danych MBo i MBw przeliczenie głównego raportu "KOREKTY_MB_MC" weryfikującego popranwość wykonanych działań.']


	first_point=[('Zatwierdzanie danych v1','Uruchomienie zatwierdzania formuł mocowych/obliczeniowych, a następnie zatwierdzenie wszystkie MBo'),
	('Generacja kodów v1','Uruchomienie programu do wyszukiwania braków i prognoz, danych niepewnych oraz PPE z brakiem schematów taryfowych'),
	('Obliczanie innZR v1','Uruchomienie zadania złożonego obliczającego innZRY odbiorcze dla wszystkich MB'),
	('Ręczna korekta kodów (Klepanie) v1','Weryfikacja kompletności danych na podstawie wcześniej wygenerowanej listy kodów PPE dla klepania V1'),
	('Kopiowanie przeliczonych innZR','Kopiowanie wcześniej przeliczonych plików innZRY do odpowiednich lokalizacji na ST2')]

	second_time=[('Agregacja MB i MDD','Wyłaczenie R&R i agregacja wpierw wszystkich MB, a następnie wszystkich MDD'),
	('Generacja kodów v2','Uruchomienie programu do wyszukiwania problematycznych kodów'),
	('Obliczanie innZR v2','Uruchomienie zadania złożonego liczącego innZRY odbiorcze dla wszystkich MB'),
	('Ręczna korekta kodów (Klepanie) v2','Ostateczna weryfikacja kompletności danych na podstawie wygenerowanej listy kodów PPE'),
	('Raport MB vs MDD','Przeliczenie raportu weryfikującego popranwość sumy agregatów MDD z agregatem MB'),
	('Weryfikacja innZR','Sprawdzenie przeliczonych wcześniej raportów innZRY dla MBo czy suma wolumenów PPE jest równa agregatowi MB oraz skopiowanie ich do odpowienich lokalizacji na ST2')	]

	third_point=[('Zatwierdzenie danych v1','Uruchomienie zatwierdzania formuł mocowych/obliczeniowych, a następnie wykonanie zatwierdzania wszystkich MBw'),
	('Agregacja v1','Wykonanie agregatów dla wszystkich MBw'),
	('Raporty innZR','Wykonanie raportów innZRY dla wszystkich MBw, sprawdzenie kompletności danych i zapisanie ich do odpowiednich lokalizacji (kompletność danych będzie można sprawdzić również wykorzystując program analogicznie jak przy OO)')]

	forth_point=[('Zatwierdzenie danych v2','Uruchomienie zatwierdzania formuł mocowych/obliczeniowych, a następnie wykonanie zatwierdzania wszystkich MBw'),
	('Agregacja v2','Wykonanie agregatów dla wszystkich MBw'),
	('Raporty innZR','Wykonanie raportów innZRY dla wszystkich MBw, ostateczne sprawdzenie kompletność danych i zapisanie plików w odpowiednich lokalizacjach (kompletność danych będzie można sprawdzić również wykorzystując program analogicznie jak przy OO)')]

	fifth_point=[('Generacja kodów OO','Uruchomienie programu do wyselekcjonowania listy kodów PPE do weryfikacji'),
	('Ręczna korekta kodów OO (Klepanie)','Sprawdzamy poprawność konfiguracji handlowej i technicznej (czy daty początku danych w innop są tożsame z konfiguracją handlową)'),
	('Ponowna Agregacja OO','Dla MB z korygowaną konfiguracją ponowne wykonanie agregatów (warto zapisywać sobie jaki SE był w zmienianym PPE tak aby nie agregować wszystkich OO danego MB)'),
	('Raporty innZRY','Przeliczenie raportów innZRY OO, sprawdzenie zgodność sum PPE z agregatami poszczególnych MB i zapisanie innZRY plików w odpowiednich lokalizacjach')]

	sixth_point=[]

	points=[first_point, second_time, third_point, forth_point, fifth_point, sixth_point]
	p_count=0
	proc_id=create_process_template(user, cor_data, cor, cor_data_end)
	for name, desc in zip(tasks_names_list, tasks_desc_list):
		task_id=create_task_template(user, proc_id, cor_data, cor_data_end, name, desc)
		for point in points[p_count]:
			create_point_template(user, proc_id, cor_data, cor_data_end, point[0], point[1], task_id)
		p_count += 1

def create_process_template(user, cor_data, cor, cor_data_end):
	data_dict={
		'proc_author':user,
		'proc_process_name': 'Przygotowanie korekta ' + cor + ' (' + cor_data.strftime("%Y-%m")+ ')',
		'proc_description' : 'Prace związane z przygotowaniem danych w celu wysłania ich na Rynek Bilansujący w korekcie '  + cor + ', dotyczy miesiąca ' + cor_data.strftime("%Y-%m"),
		'proc_start_date' : cor_data,
		'proc_end_date' : cor_data_end,
		'proc_category' : category.objects.get(cat_name='Korekty'),
		'proc_is_active':True,
		'proc_is_private':False,
		'proc_is_deleted':False,
		'proc_assigned' : user}
	new_proc_id=process.save_proc_template(data_dict)
	return new_proc_id


def create_task_template(user, proc_id, cor_data, cor_data_end, name, desc):

	first_point=[('Zatwierdzanie danych v1','Uruchamiamy zatwierdzanie formuł mocowych/obliczeniowych a następnie zatwierdzamy wszystkie MBo'),
	('Generacja kodów v1','Uruchamiamy program do wyszukiwania braków i prognoz, danych niepewnych oraz PPE z brakiem schematów taryfowych'),
	('Obliczanie innZR v1','Uruchamiamy zadanie złożone obliczające innZRY odbiorcze dla wszystkich MB'),
	('Klepanie kodów v1','Weryfikujemy kompletność danych na podstawie wcześniej wygenerowanej listy kodów PPE dla klepania V1'),
	('Kopiowanie przeliczonych innZR','Kopiujemy wcześniej przeliczone innZRY do odpowiednich lokalizacji na ST2')]

	second_time=[('Agregacja MB i MDD','Wyłaczenie R&R i agregacja wpierw wszystkich MB, a następnie wszystkich MDD'),
	('Generacja kodów v2','Uruchamiamy program do wyszukiwania problematycznych kodów'),
	('Obliczanie innZR v2','Uruchamiamy zadanie złożone liczące innZRY odbiorcze dla wszystkich MB'),
	('Klepanie kodów v2','Ostateczna weryfikacja kompletności danych na podstawie wygenerowanejlisty kodów PPE'),
	('Raport MB vs MDD','Przeliczenie raportu weryfikującego popraność czy suma agregatów MDD jest równa agregatowi MB'),
	('Weryfikacja innZR','Sprawdzenie przeliczonych wcześniej raportów innZR dla MBo czy suma PPE jest równa agregatowi MB i skopiowanie ich w odpowienie lokalizacjie na ST2')	]

	third_point=[('Zatwierdzenie danych v1','Uruchamiamy zatwierdzanie formuł mocowych/obliczeniowych a następnie zatwierdzaniem wszystkich MBw'),
	('Agregacja v1','Uruchamiamy agregaty dla wszystkich MBw'),
	('Raporty innZR','Uruchamiamy raporty innZRY dla wszystkich MBw, sprawdzamy kompletność danych i zapisujemy je do odpowiednich lokalizacji (kompletność danych będzie można sprawdzić również wykorzystując program analogicznie jak przy OO)')]

	forth_point=[('Zatwierdzenie danych v2','Uruchamiamy zatwierdzanie formuł mocowych/obliczeniowych a następnie zatwierdzaniem wszystkich MBw'),
	('Agregacja v2','Uruchamiamy agregaty dla wszystkich MBw'),
	('Raporty innZR','Uruchamiamy raporty innZRY dla wszystkich MBw, ostatecznie sprawdzamy kompletność danych i zapisujemy je do odpowiednich lokalizacji (kompletność danych będzie można sprawdzić również wykorzystując program analogicznie jak przy OO)')]

	fifth_point=[('Generacja kodów OO','Uruchamiamy program do wyselekcjonowania listy kodów PPE do weryfikacji'),
	('Klepanie kodów OO','Sprawdzamy poprawność konfiguracji handlowej i technicznej (czy daty początku danych w innop są tożsame z konfiguracją handlową)'),
	('Ponowna Agregacja OO','Dla MB dla których musieliśmy poprawić konfigurację ponownie wykonujemy agregaty (warto zapisywać sobie jaki SE był w zmienianym PPE tak aby nie agregować wszystkich OO danego MB)'),
	('Raporty innZRY','Przeliczamy innZRY OO, sprawdzamy zgodność sum PPE z agregatem MB i zapisujemy innZRY do odpowiednich lokalizacji')]


	data_dict={
		'tasks_name':name,
		'tasks_description':desc,
		'tasks_start_date':cor_data,
		'tasks_end_date':cor_data_end,
		'tasks_is_active':True,
		'tasks_is_deleted':False,
		'tasks_proc':process.objects.get(pk=proc_id)}
	new_task_id=tasks.save_task_template(data_dict)

	return new_task_id



def create_point_template(user, proc_id, cor_data, cor_data_end, name, desc, task_id):
	data_dict={
		'tasks_name':name,
		'tasks_description':desc,
		'tasks_start_date':cor_data,
		'tasks_end_date':cor_data_end,
		'tasks_is_active':True,
		'tasks_is_deleted':False,
		'tasks_proc':process.objects.get(pk=proc_id),
		'tasks_tasks':tasks.objects.get(pk=task_id)}
	new_point_id=tasks.save_task_template(data_dict)
