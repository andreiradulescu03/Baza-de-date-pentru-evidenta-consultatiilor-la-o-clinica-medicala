# Baza de date pentru evidența consultațiilor la o clinică medicală

## 1. Descrierea cerințelor
	Acest proiect urmărește dezvoltarea unei aplicații pentru gestionarea unei baze de date medicale. 
	Funcționalitățile principale includ:
		• Adăugarea, ștergerea și actualizarea înregistrărilor în tabele.
		• Executarea interogărilor simple și complexe pentru extragerea datelor relevante.
		• Utilizarea constrângerilor de integritate pentru a menține corectitudinea datelor.
		• Implementarea unei interfețe grafice pentru interacțiunea cu utilizatorii. 
	
	Aplicația respectă cerințele privind utilizarea a minimum 6 interogări simple cu JOIN-uri și 4 interogări complexe cu subcereri.

## 2. Etapa de proiectare
	Proiectarea bazei de date a fost realizată folosind o diagramă ER, care detaliază relațiile dintre tabele. 
	Diagrama conține următoarele tabele principale: **Pacienti**, **Medici**, **Consultatii**, **Specialitati**, **Servicii_Medicale** și **Consultatie_Servicii**. 
	Relațiile dintre acestea sunt definite pe baza cheilor primare și externe.

## 3. Descrierea tabelelor și a relațiilor

### a. Tabel: Pacienti
	- **Id_pacient**: INT - Cheie primară (PK), generată automat prin `IDENTITY(1000,1)`
	- **Nume**: VARCHAR(50) - Numele pacientului
	- **Prenume**: VARCHAR(50) - Prenumele pacientului
	- **DataNasterii**: DATE - Data nașterii (mai mică decât data curentă)
	- **Telefon**: VARCHAR(15) - Număr de telefon (UNIQUE), cu minimum 10 caractere
	- **Email**: VARCHAR(100) - Adresa de e-mail (UNIQUE), validată cu expresia `([email] like '%_@__%.%')`

### b. Tabel: Medici
	- **Id_medic**: INT - Cheie primară (PK), generată automat prin `IDENTITY(100,1)`
	- **Nume**: VARCHAR(50) - Numele medicului
	- **Prenume**: VARCHAR(50) - Prenumele medicului
	- **Id_specialitate**: INT - Cheie externă (FK) către `Specialitati.id_specialitate`
	- **Telefon**: VARCHAR(15) - Număr de telefon (UNIQUE), cu minimum 10 caractere
	- **Email**: VARCHAR(50) - Adresa de e-mail (UNIQUE), validată cu expresia `([email] like '%_@__%.%')`

### c. Tabel: Specialitati
	- **Id_specialitate**: INT - Cheie primară (PK), generată automat prin `IDENTITY(10,1)`
	- **Nume**: VARCHAR(50) - Numele specialității medicale (de exemplu, Cardiologie, Dermatologie) (UNIQUE)

### d. Tabel: Consultatii
	- **Id_consultatie**: INT - Cheie primară (PK), generată automat prin `IDENTITY(10000,1)`
	- **Id_pacient**: INT - Cheie externă (FK) către `Pacienti.id_pacient`
	- **Id_medic**: INT - Cheie externă (FK) către `Medici.id_pacient`
	- **Data_consultatie**: DATETIME - Data și ora consultației (valoare implicită: data curentă)
	- **Diagnosticul**: TEXT - Descrierea diagnosticului
	- **Tratament**: TEXT - Detalii despre tratament (opțional)
	- **Cost**: DECIMAL(10,2) - Costul consultației

### e. Tabel: Servicii_Medicale
	- **Id_serviciu**: INT - Cheie primară (PK), generată automat prin `IDENTITY(2000,1)`
	- **Nume**: VARCHAR(100) - Denumirea serviciului medical (UNIQUE)
	- **Pret**: DECIMAL(10,2) - Prețul serviciului

### f. Tabel: Consultatie_Servicii
	- **Id_consultatie**: INT - Cheie externă (FK) către `Consultatii.id_consultatie`
	- **Id_serviciu**: INT - Cheie externă (FK) către `Servicii_Medicale.id_serviciu`
	- **Cantitate**: INT - Cantitatea de servicii oferite în cadrul consultației

#### Relațiile dintre tabele
1. Relația dintre **Pacienti** și **Consultatii**: 1 la N  
		Fiecare pacient poate avea mai multe consultații, dar o consultație este asociată cu un singur pacient.
2. Relația dintre **Medici** și **Consultatii**: 1 la N  
		Fiecare medic poate efectua mai multe consultații, dar fiecare consultație este realizată de un singur medic.
3. Relația dintre **Specialitati** și **Medici**: 1 la N  
		O specialitate medicală poate fi practicată de mai mulți medici, dar un medic are o singură specialitate.
4. Relația dintre **Consultatii** și **Servicii_Medicale** prin **Consultatie_Servicii**: N la N  
		O consultație poate include mai multe servicii medicale, iar un serviciu medical poate fi oferit în cadrul mai multor consultații. 
		Tabelul de legătură **Consultatie_Servicii** gestionează relația dintre aceste tabele.

## 4. Constrângerile de integritate
	Pentru a menține integritatea bazei de date, au fost impuse următoarele constrângeri:
		• Chei primare unice pentru fiecare tabel.
		• Chei externe pentru a lega înregistrările între tabele (ex. PacientID în Consultatii este cheie externă).
		• Constrângeri CHECK pentru validarea datelor (ex. DataConsultatie să nu fie în trecut exagerat).
		• Constrângeri NOT NULL pentru a asigura completarea câmpurilor esențiale.

## 5. Funcționarea aplicației
	Aplicația include o interfață grafică dezvoltată în Python folosind Tkinter. Funcționalitățile sunt structurate astfel:
		• Meniul principal oferă acces la fiecare tabel și la interogările predefinite.
		• Funcționalitățile **Adaugă**, **Șterge** și **Actualizează** sunt disponibile pentru fiecare tabel.
		• Interogările sunt organizate în două categorii: **Simple** și **Complexe**. 
		• Aplicația include un sistem de autentificare pentru utilizatori, cu validarea username-ului și parolei.

## 6. Interogări simple
	Lista interogărilor simple implementate, fiecare având cel puțin 2 JOIN-uri:
		• Consultatii și Medici cu Specialitati.
		• Pacienti și Servicii Medicale.
		• Medici cu Specialitati și Pacienti.
		• Consultatii recente și costuri.
		• Servicii utilizate de Pacienti.
		• Pacienti și număr consultații.

## 7. Interogări complexe
	Lista interogărilor complexe implementate, fiecare având cel puțin 2 subcereri:
		• Pacienți cu mai mult de X consultații, unde X este parametrul variabil.
		• Medici cu consultații peste media costurilor.
		• Consultații și servicii sub media costurilor.
		• Pacienți care folosesc mai mult de 3 servicii unice.
