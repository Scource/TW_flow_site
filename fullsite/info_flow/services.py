from .models import tasks, process, comments, category
from .permissions import add_perms_to_new_object, toggle_perm_on_object
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

	#proc name/desc data
	standard_cor=[('Przygotowanie korekty ' + cor + ' (' + cor_data.strftime("%Y-%m")+ ')'),
	('Prace związane z przygotowaniem danych w celu wysłania ich na Rynek Bilansujący w korekcie '  + cor + ', dotyczy miesiąca ' + cor_data.strftime("%Y-%m"))]

	#UDPS data
	UDPS_task=['Podczyt UDPS', 'Zadania związane z zaimportowaniem danych zużyciowych z systemu bilingowego do systemu innOP']

	#standard coorrections tasks
	tasks_names_list=['MB Odbiorcze  v1', 'MB Odbiorcze  v2', 'MB Wytwórcze  v1', 'MB Wytwórcze  v2', 'Weryfikacja Odbiorczego Oddania', 'Raport "KOREKTY_MB_MC"', 'Prace do wykonania w aplikacji WIRE']
	tasks_desc_list=['Zadania związane z przygotowaniem danych w celu wysłania na Rynek Bilansujący MB odbiorczych.',
	'Dodatkowa iteracja zadań związane z przygotowaniem danych w celu wysłania na Rynek Bilansujący MB odbiorczych.',
	'Zadania związane z przygotowaniem danych w celu wysłania na Rynek Bilansujący MB wytwórczych.',
	'Dodatkowa iteracja zadań związanych z przygotowaniem danych w celu wysłania na Rynek Bilansujący MB wytwórczych.',
	'Sprawdzenie konfiguracji technicznej i handlowej dla wszystkich MBo na kierunku oddanie dla prosumentów/mikroinstalacji.',
	'Po zakończeniu wcześniejszych prac związanych z weryfikacją danych MBo i MBw przeliczenie głównego raportu "KOREKTY_MB_MC" weryfikującego popranwość wykonanych działań.',
	'Zadania związane z przygotowaniem i wysłaniem dokumentów DGMB w WIRE']

	#standard coorrections points
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
	seventh_point=[('Import danych do WIRE', 'Zaimportowanie danych z systemu innOP do bazy WIRE dla korygowanych MBo i MBw'),
	('Generacja dokumentów DGMB','Utworzenie dokumentów DGMB dla korygowanych MB'),
	('Generacja raportów Dobowo-Godzinnych','Utworzenie i wyeksportowanie raportów Dobowo-Godzinnych dla korygowanych MBo i MBw'),
	('Ostateczna weryfikacja danych WIRE vs INNOP','Przy pomocy programiku sprawdzamy czy to co jest w WIRE jest równe temu co jest w bazie innOP. Sprawdzamy również czy nie ma żadnych pików itp'),
	('Wystawienie dokumentów DGMB','Nastawiamy w WIRE dokumenty DGMB do wysłania na odpowiedni dzień i godzinę')]

	points=[first_point, second_time, third_point, forth_point, fifth_point, sixth_point, seventh_point]

	#proc data used in m14 correction temple
	m14_proc=['Przygotowanie korekty ' + cor + ' (' + cor_data.strftime("%Y-%m")+ ')','Prace związane z przygotowaniem danych do wysłania na Rynek Bilansujący w korekcie M+15, która odbędzie się w następnym miesiącu']

	#task data used in m14 correction temple
	m14_task=['MB Odbiorcze', 'Zadania związane z przygotowaniem danych w celu wysłania na Rynek Bilansujący dla MB odbiorczych']	

	#points data used in m14 correction temple
	m15_points=[('Zatwierdzanie danych', 'Zatwierdzenie formuł mocowych/obliczeniowych oraz następnie zatwierdzenie wszystkich MBo'),
	('Generacja kodów', 'Stworzenie listy braków i prognoz, danych niepewnych oraz PPE z brakiem schematów taryfowych z wykorzystaniem programu'),
	('Obliczanie innZR','Obliczenie innZR dla wszystkich MB odbiorczych z wykorzystaniem zadania złożonego'),
	('Ręczna korekta kodów (Klepanie)','Weryfikacja kompletności danych na podstawie wcześniej wygenerowanej listy kodów PPE do weryfikacji'),
	('Kopiowanie przeliczonych raportów innZRY','Kopiowanie wcześniej przeliczonych plików innZRY do odpowiednich lokalizacji na ST2')]
		
	p_count=0
	if cor=='M+14':
		proc_id=process_template(user, cor_data, cor, cor_data_end, m14_proc)

		task_id=task_template(user, proc_id, cor_data, cor_data_end, m14_task[0], m14_task[1])
		add_perms_to_new_object(user, tasks.objects.get(pk=task_id), 'task')
		for point in m15_points:
			point_id=point_template(user, proc_id, cor_data, cor_data_end, point[0], point[1], task_id)
			add_perms_to_new_object(user, tasks.objects.get(pk=point_id), 'task')
	else:
		proc_id=process_template(user, cor_data, cor, cor_data_end, standard_cor)
		if cor=='M+4':
			m4_task_id=task_template(user, proc_id, cor_data, cor_data_end, UDPS_task[0], UDPS_task[1])
			add_perms_to_new_object(user, tasks.objects.get(pk=m4_task_id), 'task')
		for name, desc in zip(tasks_names_list, tasks_desc_list):
			task_id=task_template(user, proc_id, cor_data, cor_data_end, name, desc)
			add_perms_to_new_object(user, tasks.objects.get(pk=task_id), 'task')
			for point in points[p_count]:
				point_id=point_template(user, proc_id, cor_data, cor_data_end, point[0], point[1], task_id)
				add_perms_to_new_object(user, tasks.objects.get(pk=point_id), 'task')
			p_count += 1
	add_perms_to_new_object(user, process.objects.get(pk=proc_id), 'proc')
	return proc_id

def process_template(user, cor_data, cor, cor_data_end, proc_data):
	data_dict={
		'proc_author':user,
		'proc_process_name': proc_data[0],
		'proc_description' : proc_data[1],
		'proc_start_date' : cor_data,
		'proc_end_date' : cor_data_end,
		'proc_category' : category.objects.get(cat_name='Korekty'),
		'proc_is_active':True,
		'proc_is_private':False,
		'proc_is_deleted':False,
		'proc_assigned' : user}
	new_proc_id=process.save_proc_template(data_dict)
	return new_proc_id

def task_template(user, proc_id, cor_data, cor_data_end, name, desc):
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

def point_template(user, proc_id, cor_data, cor_data_end, name, desc, task_id):
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
	return new_point_id

def create_OSDN_template(user, cor_data):
	cor_data_end=cor_data.replace(day=calendar.monthrange(cor_data.year, cor_data.month)[1], hour=23, minute=59)

	#osdn_proc=['Uzgadnianie obszarów OSDn','Prace związane z przygotowaniem i uzgodnieniem poprawnych danych pochodzących z obszarów OSDn']

	#osdn task data
	osdn_task=[('Import danych z serwerów sFTP/FTP','Zaimportowanie do systemu InnOP plików wystawianych na serwery FTP/sFTP przez poszczególne OSDn'),
	('Zatwierdzanie i sprawdzenie danych','Zatwierdzenie danych dla wszystkich trybów korekt i ich weryfikacja'),
	('D-ENERGIA (ZACHEM)','Uzgodnienie danych z OSDn'),
	('Green Lights GLDS','Uzgodnienie danych z OSDn'),
	('Grupa Energia GEGE','Uzgodnienie danych z OSDn'),
	('Grupa Energia Obrót GEOG','Uzgodnienie danych z OSDn'),
	('POLENERGIA DYSTRYBUCJA','Uzgodnienie danych z OSDn'),
	('POWER21','Uzgodnienie danych z OSDn'),
	('TERAWAT DYSTRYBUCJA','Uzgodnienie danych z OSDn'),
	('ZMPSIŚ','Uzgodnienie danych z OSDn'),
	('EC BYDGOSZCZ','Uzgodnienie danych z OSDn'),
	('HCP','Uzgodnienie danych z OSDn'),
	('Potestia (POTS)','Uzgodnienie danych z OSDn'),
	('PKP','Uzgodnienie danych z OSDn')]

	#osdn points data
	point1=[]
	point2=[('Zatwierdzanie danych','Wykonanie zatwierdzania formuł obliczeniowych i profili mocowych dla wszystkich korekt'),
	('Sprawdzenie danych','Sprawdzenie czy suma wszystkich formuł mocowych jest równa SUMIE TPA')]
	point3=[('Raport','Przeliczenie raportu odbiorców przypisanych do OSDn'),
	('Przesłanie informacji do OSDn','Kontakt z OSDn w celu sprawdzenia i akceptacji poprawności danych w systemie InnOP'),
	('Potwierdzenie od OSDn', 'Uzyskanie informacji o zgodności danych')]

	points=[point1, point2, point3, point3, point3, point3, point3, point3, point3, point3, point3, point3, point3, point3]

	proc_id=OSDN_process_template(user, cor_data, cor_data_end)
	add_perms_to_new_object(user, process.objects.get(pk=proc_id), 'proc')
	p_count=0
	for task in osdn_task:
		task_id=task_template(user, proc_id, cor_data, cor_data_end, task[0], task[1])
		add_perms_to_new_object(user, tasks.objects.get(pk=task_id), 'task')
		for point in points[p_count]:
			point_id=point_template(user, proc_id, cor_data, cor_data_end, point[0], point[1], task_id)
			add_perms_to_new_object(user, tasks.objects.get(pk=point_id), 'task')
		p_count += 1
	return proc_id

def OSDN_process_template(user, cor_data, cor_data_end):
	data_dict={
		'proc_author':user,
		'proc_process_name': 'Uzgadnianie obszarów OSDn',
		'proc_description' : 'Prace związane z przygotowaniem i uzgodnieniem poprawnych danych pochodzących z obszarów OSDn',
		'proc_start_date' : cor_data,
		'proc_end_date' : cor_data_end,
		'proc_category' : category.objects.get(cat_name='Korekty'),
		'proc_is_active':True,
		'proc_is_private':False,
		'proc_is_deleted':False,
		'proc_assigned' : user}
	new_proc_id=process.save_proc_template(data_dict)
	return new_proc_id

