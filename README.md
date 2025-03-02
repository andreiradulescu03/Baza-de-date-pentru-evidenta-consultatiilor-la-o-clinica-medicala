Baza de date pentru evidenta consultatiilor la o clinica medicala
1.	Descrierea cerintelor
	Acest proiect urmareste dezvoltarea unei aplicatii pentru gestionarea unei baze de date medicale. Functionalitatile principale includ:
		•	Adaugarea, stergerea si actualizarea inregistrarilor in tabele.
		•	Executarea interogarilor simple si complexe pentru extragerea datelor relevante.
		•	Utilizarea constrangerilor de integritate pentru a mentine corectitudinea datelor.
		•	Implementarea unei interfete grafice pentru interactiunea cu utilizatorii. Aplicatia respecta cerintele privind utilizarea a minim 6 interogari simple cu JOIN-uri si 4 interogari complexe cu subcereri.
2.	Etapa de proiectare
	Proiectarea bazei de date a fost realizata folosind o diagrama ER, care detaliaza relatiile dintre tabele. Diagrama contine urmatoarele tabele principale: Pacienti, Medici, Consultatii, Specialitati, ServiciiMedicale si ConsultatieServicii. Relatiile dintre acestea sunt definite pe baza cheilor primare si externe.
 
3.	Descrierea tabelelor si a relatiilor
________________________________________
	a.	Tabel: Pacienti
		o	Id_pacient: INT - Cheie primara (PK), generata automat prinIDENTITY(1000,1)
		o	Nume: VARCHAR(50) - Numele pacientului
		o	Prenume: VARCHAR(50) - Prenumele pacientului
		o	DataNasterii: DATE - Data nasterii (mai mica decat data curenta)
		o	Telefon: VARCHAR(15) - Numar de telefon (UNIQUE), cu minim 10 caractere
		o	Email: VARCHAR(100) - Adresa de e-mail (UNIQUE), formatat cu expresia ([email] like '%_@__%.%') 
________________________________________
	b.	Tabel: Medici
		o	Id_medic: INT - Cheie primara (PK), generata automat prin IDENTITY(100,1)
		o	Nume: VARCHAR(50) - Numele medicului
		o	Prenume: VARCHAR(50) - Prenumele medicului
		o	Id_specialitate: INT - Cheie externa (FK) catre Specialitati.id_specialitate
		o	Telefon: VARCHAR(15) - Numar de telefon (UNIQUE), cu minim 10 caractere
		o	Email: VARCHAR(50) - Adresa de e-mail (UNIQUE), formatat cu expresia ([email] like '%_@__%.%')
________________________________________
	c.	Tabel: Specialitati
		o	Id_specialitate: INT - Cheie primara (PK), generata automat prin IDENTITY(10,1)
		o	Nume: VARCHAR(50) - Numele specialitatii medicale (de exemplu, Cardiologie, Dermatologie) (UNIQUE)
________________________________________
	d.	Tabel: Consultatii
		o	Id_consultatie: INT - Cheie primara (PK), generata automat prin IDENTITY(10000,1)
		o	Id_pacient: INT - Cheie externa (FK) catre Pacienti.id_pacient
		o	Id_medic: INT - Cheie externa (FK) catre Medici.id_pacient
		o	Data_consultatie: DATETIME - Data si ora consultatiei (valoare implicita: data curenta)
		o	Diagnosticul: TEXT - Descrierea diagnosticului
		o	Tratament: TEXT - Detalii despre tratament (optional)
		o	Cost: DECIMAL(10,2) - Costul consultatiei
________________________________________
	e.	Tabel: Servicii_Medicale
		o	Id_serviciu: INT - Cheie primara (PK), generata automat prin IDENTITY(2000,1)
		o	Nume: VARCHAR(100) - Denumirea serviciului medical (UNIQUE)
		o	Pret: DECIMAL(10,2) - Pretul serviciului
________________________________________
	f.	Tabel: Consultatie_Servicii
		o	Id_consultatie: INT - Cheie externa (FK) catre Consultatii.id_consultatie
		o	Id_serviciu: INT - Cheie externa (FK) catre ServiciiMedicale.id_serviciu
		o	Cantitate: INT - Cantitatea de servicii oferite in cadrul consultatiei
Relatiile dintre tabele
1.	Relatia dintre Pacienti si Consultatii: 1 la N
	Fiecare pacient poate avea mai multe consultatii, dar o consultatie este asociata cu un singur pacient.
2.	Relatia dintre Medici si Consultatii: 1 la N
	Fiecare medic poate efectua mai multe consultatii, dar fiecare consultatie este realizata de un singur medic.
3.	Relatia dintre Specialitati si Medici: 1 la N
	O specialitate medicala poate fi practicata de mai multi medici, dar un medic are o singura specialitate.
4.	Relatia dintre Consultatii si Servicii_Medicale prin ConsultatieServicii: N la N
	O consultatie poate include mai multe servicii medicale, iar un serviciu medical poate fi oferit in cadrul mai multor consultatii. Tabelul de legatura Consultatie_Servicii gestioneaza relatia dintre aceste tabele.
4.	Constrangerile de integritate
	Pentru a mentine integritatea bazei de date, au fost impuse urmatoarele constrangeri:
		•	Chei primare unice pentru fiecare tabel.
		•	Chei externe pentru a lega inregistrarile intre tabele (ex. PacientID in Consultatii este cheie externa).
		•	Constrangeri CHECK pentru validarea datelor (ex. DataConsultatie sa nu fie in trecut exagerat).
		•	Constrangeri NOT NULL pentru a asigura completarea campurilor esentiale.

5.	Functionarea aplicatiei
		Aplicatia include o interfata grafica dezvoltata in Python folosind Tkinter. Functionalitatile sunt structurate astfel:
			•	Meniul principal ofera acces la fiecare tabel si la interogarile predefinite.
			•	Functionalitatile Adauga, Sterge si Actualizeaza sunt disponibile pentru fiecare tabel.
			•	Interogarile sunt organizate in doua categorii: Simple si Complexe. De asemenea, aplicatia include un sistem de autentificare pentru utilizatori, cu validarea username-ului si parolei.

6.	Interogari simple
		Lista interogarilor simple implementate, fiecare avand cel putin 2 JOIN-uri:
			•	Consultatii si Medici cu Specialitati.
			•	Pacienti si Servicii Medicale.
			•	Medici cu Specialitati si Pacienti.
			•	Consultatii recente si costuri.
			•	Servicii utilizate de Pacienti.
			•	Pacienti si numar consultatii.

7.	Interogari complexe
		Lista interogarilor complexe implementate, fiecare avand cel putin 2 subcereri:
			•	Pacienti cu mai mult de X consultatii, unde X este parametrul variabil.
			•	Medici cu consultatii peste media costurilor.
			•	Consultatii si servicii sub media costurilor.
			•	Pacienti care folosesc mai mult de 3 servicii unice.


