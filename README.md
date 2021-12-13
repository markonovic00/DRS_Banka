# DRS_Banka

# DRS_Projekat

Teams Meeting: https://teams.microsoft.com/l/meetup-join/19%3ameeting_MmRiMDY3ZDItMTA5MC00YWU2LWEzNmEtYWNkZjIxZjJjYjQ0%40thread.v2/0?context=%7b%22Tid%22%3a%22ada575f6-4e91-4d1d-aa89-9b2d9f5810e3%22%2c%22Oid%22%3a%22a8076ea6-1565-4064-b3f2-d417ad36a00b%22%7d

Projektni zadatak DRES

Implementirati projekat koji simulira medjunarodni platni promet I on-line racun za licne uplate.

Implementacija treba da sadrzi 3 komponente:

    1. Korisnicki interfejs (UI)
    2. Servis za obradu zahteva I podataka (Engine)
    3. Bazu podataka (DB)

Korisnicki interfejs (UI)

Korisnicki interfejs je Flask web aplikacija koja treba da opsluzi korisnika u interakciji sa platnim prometom. 

Akcije koje treba podrzati na korisnickom interfejsu su:

    1. Registracija novog korisnika
    2. Logovanje postojeceg korisnika
    3. Izmena korisnickog profila
    4. Pregled stanja
    5. Ubacivanje sredstava putem platne kartice na on-line racun
    6. Pregled istorije transakcija sa mogucnoscu sortiranja I filtriranja
    7. Iniciranje nove transakcije drugom korisniku
        a. Koji ima otvoren on-line racun
        b. Na racun u banci
    8. Izbor valute – sa osvezavanjem kursne liste sa interneta
    9. Zamena valute

Korisnik se registruje unoseci:
    1. Ime
    2. Prezime
    3. Adresa
    4. Grad
    5. Drzava
    6. Broj telefona
    7. Email
    8. Lozinka

Korisnike se loguje putem:
    • Email
    • Lozinka

Novi korisnik ima stanje 0. On tada treba da zatrazi verifikaciju naloga. Za verifikaciju je potrebno da unese svoju platnu karticu I bice mu skinuto 1$. Nakon toga korisnik moze da uplati sredstva sa kartice na svoj on-line racun.

Test platna kartica:

Broj: 4242 4242 4242 4242
Ime: <Ime Korisnika>
Datum isteka kartice: 02/23
Sigurnosni kod: 123

Korisnik inicira transakciju drugom korisniku unoseci podatke o racunu korisnika u banci ili njegovoj email adresi ukoliko drugi korisnik ima registrovan nalog.

Kad se inicira transakcija, ona treba da se obradi na strain Engine-a. Transakcija ima stanja:

    1. U obradi
    2. Obradjeno
    3. Odbijeno

Potrebno vreme da se transakcija odobri je 2min. Za to vreme sistem mora da bude sposoban da odgovori na ostale zahteve.

Konverzija valute se vrsi po principu da korisnik uplacuje sa kartice sa on-line racun u Dinarima. Kursna lista se dovlaci sa eksternog API-a kursne liste. Nakon dobijanja liste, korisnik bira valutu I iznos. Nakon uspesne konverzije korisnik ima novo stanje u novoj valuti. Korisnik moze da ima neogranicen broj valuta I stanja racuna u valutama.
Servis za obradu zahteva I podataka (Engine)

Engine je servis implementiran kao flask API aplikacija. Engine ima svoje endpointe koje prikazuje eksternom svetu (UI aplikaciji) za koriscenje. UI deo poziva endpointe Engine-a radi obrade raznih zahteva I podataka. Pri tome samo Engine komunicira sa bazom, a UI sa Engine-om.

Baza podataka (DB)

Baza podataka je u komunikaciji sa Engine-om za svrhu skladistenja podataka o aplikaciji. U bazi se skladiste svi esencijalno bitni podaci za rad aplikacije. 

Model baze kao I tip baze (NoSQL, SQL) je proizvoljan.





Nacina ocenjivanja

    1. Aplikacija je funkcionalna I postoji Flask aplikacija – 51 poen
        a. Aplikacija se sastoji od 1 aplikacije bez baze koja je potpuno funkcionalna
    2. Implementiran Engine kao posebna Flask aplikacija gde UI komunicira sa Engine-om putem API-a – 10 poena
    3. Implementirana je baza sa kojom komunicira Engine – 9 poena
    4. Koriscenje niti prilikom implementacije – 10 poena
    5. Koriscenje procesa prilikom implementacije – 10 poena
    6. Dokerizacija aplikacije I pokretanje na vise racunara (distribuiran sistem) – 10 poena

    • Deploy aplikacije na Heroku – gratis 5 poena (moguce samo ako je svih 6 tacaka implementirano)

