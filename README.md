# Baza de date pentru evidenta consultatiilor la o clinica medicala

## 1. Descrierea cerintelor
	Acest proiect urmareste dezvoltarea unei aplicatii pentru gestionarea unei baze de date medicale. 
	Functionalitatile principale includ:
		• Adaugarea, stergerea si actualizarea inregistrarilor in tabele.
		• Executarea interogarilor simple si complexe pentru extragerea datelor relevante.
		• Utilizarea constrangerilor de integritate pentru a mentine corectitudinea datelor.
		• Implementarea unei interfete grafice pentru interactiunea cu utilizatorii.
	
	Aplicatia respecta cerintele privind utilizarea a minimum 6 interogari simple cu JOIN-uri si 4 interogari complexe cu subcereri.

## 2. Etapa de proiectare
	Proiectarea bazei de date a fost realizata folosind o diagrama ER, care detaliaza relatiile dintre tabele. 
	Diagrama contine urmatoarele tabele principale: **Pacienti**, **Medici**, **Consultatii**, **Specialitati**, **Servicii_Medicale** si **Consultatie_Servicii**. 
	Relatiile dintre acestea sunt definite pe baza cheilor primare si externe.

## 3. Descrierea tabelelor si a relatiilor

### a. Tabel: Pacienti
	- **Id_pacient**: INT - Cheie primara (PK), generata automat prin `IDENTITY(1000,1)`
	- **Nume**: VARCHAR(50) - Numele pacientului
	- **Prenume**: VARCHAR(50) - Prenumele pacientului
	- **DataNasterii**: DATE - Data nasterii (mai mica decat data curenta)
	- **Telefon**: VARCHAR(15) - Numar de telefon (UNIQUE), cu minimum 10 caractere
	- **Email**: VARCHAR(100) - Adresa de e-mail (UNIQUE), validata cu expresia `([email] like '%_@__%.%')`

### b. Tabel: Medici
	- **Id_medic**: INT - Cheie primara (PK), generata automat prin `IDENTITY(100,1)`
	- **Nume**: VARCHAR(50) - Numele medicului
	- **Prenume**: VARCHAR(50) - Prenumele medicului
	- **Id_specialitate**: INT - Cheie externa (FK) catre `Specialitati.id_specialitate`
	- **Telefon**: VARCHAR(15) - Numar de telefon (UNIQUE), cu minimum 10 caractere
	- **Email**: VARCHAR(50) - Adresa de e-mail (UNIQUE), validata cu expresia `([email] like '%_@__%.%')`

### c. Tabel: Specialitati
	- **Id_specialitate**: INT - Cheie primara (PK), generata automat prin `IDENTITY(10,1)`
	- **Nume**: VARCHAR(50) - Numele specialitatii medicale (ex. Cardiologie, Dermatologie) (UNIQUE)

### d. Tabel: Consultatii
	- **Id_consultatie**: INT - Cheie primara (PK), generata automat prin `IDENTITY(10000,1)`
	- **Id_pacient**: INT - Cheie externa (FK) catre `Pacienti.id_pacient`
	- **Id_medic**: INT - Cheie externa (FK) catre `Medici.id_pacient`
	- **Data_consultatie**: DATETIME - Data si ora consultatiei (valoare implicita: data curenta)
	- **Diagnosticul**: TEXT - Descrierea diagnosticului
	- **Tratament**: TEXT - Detalii despre tratament (optional)
	- **Cost**: DECIMAL(10,2) - Costul consultatiei

### e. Tabel: Servicii_Medicale
	- **Id_serviciu**: INT - Cheie primara (PK), generata automat prin `IDENTITY(2000,1)`
	- **Nume**: VARCHAR(100) - Denumirea serviciului medical (UNIQUE)
	- **Pret**: DECIMAL(10,2) - Pretul serviciului

### f. Tabel: Consultatie_Servicii
	- **Id_consultatie**: INT - Cheie externa (FK) catre `Consultatii.id_consultatie`
	- **Id_serviciu**: INT - Cheie externa (FK) catre `Servicii_Medicale.id_serviciu`
	- **Cantitate**: INT - Cantitatea de servicii oferite in cadrul consultatiei

#### Relatiile dintre tabele
1. Relatia dintre **Pacienti** si **Consultatii**: 1 la N  
		Fiecare pacient poate avea mai multe consultatii, dar o consultatie este asociata cu un singur pacient.
2. Relatia dintre **Medici** si **Consultatii**: 1 la N  
		Fiecare medic poate efectua mai multe consultatii, dar fiecare consultatie este realizata de un singur medic.
3. Relatia dintre **Specialitati** si **Medici**: 1 la N  
		O specialitate medicala poate fi practicata de mai multi medici, dar un medic are o singura specialitate.
4. Relatia dintre **Consultatii** si **Servicii_Medicale** prin **Consultatie_Servicii**: N la N  
		O consultatie poate include mai multe servicii medicale, iar un serviciu medical poate fi oferit in cadrul mai multor consultatii. 
		Tabelul de legatura **Consultatie_Servicii** gestioneaza relatia dintre aceste tabele.

## 4. Constrangerile de integritate
	Pentru a mentine integritatea bazei de date, au fost impuse urmatoarele constrangeri:
		• Chei primare unice pentru fiecare tabel.
		• Chei externe pentru a lega inregistrarile intre tabele (ex. PacientID in Consultatii este cheie externa).
		• Constrangeri CHECK pentru validarea datelor (ex. DataConsultatie sa nu fie in trecut exagerat).
		• Constrangeri NOT NULL pentru a asigura completarea campurilor esentiale.

## 5. Functionarea aplicatiei
	Aplicatia include o interfata grafica dezvoltata in Python folosind Tkinter. Functionalitatile sunt structurate astfel:
		• Meniul principal ofera acces la fiecare tabel si la interogarile predefinite.
		• Functionalitatile **Adauga**, **Sterge** si **Actualizeaza** sunt disponibile pentru fiecare tabel.
		• Interogarile sunt organizate in doua categorii: **Simple** si **Complexe**. 
		• Aplicatia include un sistem de autentificare pentru utilizatori, cu validarea username-ului si parolei.

## 6. Interogari simple
	Lista interogarilor simple implementate, fiecare avand cel putin 2 JOIN-uri:
		• Consultatii si Medici cu Specialitati.
		• Pacienti si Servicii Medicale.
		• Medici cu Specialitati si Pacienti.
		• Consultatii recente si costuri.
		• Servicii utilizate de Pacienti.
		• Pacienti si numar consultatii.

## 7. Interogari complexe
	Lista interogarilor complexe implementate, fiecare avand cel putin 2 subcereri:
		• Pacienti cu mai mult de X consultatii, unde X este parametrul variabil.
		• Medici cu consultatii peste media costurilor.
		• Consultatii si servicii sub media costurilor.
		• Pacienti care folosesc mai mult de 3 servicii unice.
