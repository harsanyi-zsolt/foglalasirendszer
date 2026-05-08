import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


def init_adatok_fajl():
    fajl_nev = "adatok.txt"
    if not os.path.exists(fajl_nev):
        try:
            with open(fajl_nev, "w", encoding="utf-8") as f:
                f.write("Név: Harsányi Zsolt Tamás\n")
                f.write("Szak: Mérnökinformatikus\n")
                f.write("Neptun kód: UEYE7W\n")
            print(f"[INFO] '{fajl_nev}' fájl sikeresen létrehozva.")
        except Exception as e:
            print(f"[HIBA] Nem sikerült létrehozni a fájlt: {e}")
    else:
        print(f"[INFO] '{fajl_nev}' fájl már létezik.")


class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar
        self.elerheto = True

    @abstractmethod
    def jarat_info(self):
        pass


class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegyar, repulesi_ido_perc):
        super().__init__(jaratszam, celallomas, jegyar)
        self.repulesi_ido_perc = repulesi_ido_perc

    def jarat_info(self):
        return f"[Belföldi] {self.jaratszam} -> {self.celallomas} (Ár: {self.jegyar} Ft, Idő: {self.repulesi_ido_perc} p)"


class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, celallomas, jegyar, repulesi_ido_perc):
        super().__init__(jaratszam, celallomas, jegyar)
        self.repulesi_ido_perc = repulesi_ido_perc

    def jarat_info(self):
        return f"[Nemzetközi] {self.jaratszam} -> {self.celallomas} (Ár: {self.jegyar} Ft, Idő: {self.repulesi_ido_perc} p)"


class JegyFoglalas:
    def __init__(self, foglalas_id, jarat, datum):
        self.foglalas_id = foglalas_id
        self.jarat = jarat
        self.datum = datum

    def __str__(self):
        return f"Foglalás ID: {self.foglalas_id} | Járat: {self.jarat.jaratszam} ({self.jarat.celallomas}) | Dátum: {self.datum.strftime('%Y-%m-%d')} | Ár: {self.jarat.jegyar} Ft"


class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []
        self.foglalasok = []

    def jarat_hozzaadas(self, jarat):
        self.jaratok.append(jarat)
        print(f"[INFO] Járat hozzáadva: {jarat.jaratszam}")

    def foglalas(self, jarat_index, datum_str):
        if jarat_index < 0 or jarat_index >= len(self.jaratok):
            print("[HIBA] Érvénytelen járatszám/Index!")
            return 0

        jarat = self.jaratok[jarat_index]

        if not jarat.elerheto:
            print("[HIBA] A kiválasztott járat jelenleg nem elérhető.")
            return 0

        try:
            datum = datetime.strptime(datum_str, '%Y-%m-%d').date()
        except ValueError:
            print("[HIBA] Érvénytelen dátum formátum! (Helyes formátum: ÉÉÉÉ-HH-NN)")
            return 0

        mai_datum = datetime.now().date()
        if datum < mai_datum:
            print("[HIBA] Nem lehet a múltban lévő dátumra foglalni!")
            return 0

        uj_foglalas = JegyFoglalas(str(uuid.uuid4())[:8], jarat, datum)
        self.foglalasok.append(uj_foglalas)
        print(f"[SIKER] Foglalás sikeres! ID: {uj_foglalas.foglalas_id}")
        return jarat.jegyar

    def lemondas(self, foglalas_id):
        talalt = False
        for foglalas in self.foglalasok:
            if foglalas.foglalas_id == foglalas_id:
                self.foglalasok.remove(foglalas)
                print(f"[SIKER] A '{foglalas_id}' azonosítójú foglalás lemondva.")
                talalt = True
                break

        if not talalt:
            print("[HIBA] A megadott azonosítójú foglalás nem található.")

    def foglalasok_listazasa(self):
        print(f"\n--- {self.nev} Aktív FOGLALÁSOK ({len(self.foglalasok)} db) ---")
        if not self.foglalasok:
            print("Jelenleg nincsenek aktív foglalások.")
        else:
            for idx, foglalas in enumerate(self.foglalasok, 1):
                print(f"{idx}. {foglalas}")
        print("-" * 50)

    def jaratok_listazasa(self):
        print("\n--- ELÉRHETŐ JÁRATOK ---")
        for idx, jarat in enumerate(self.jaratok, 1):
            print(f"{idx}. {jarat.jarat_info()}")
        print("-" * 30)


def main():
    init_adatok_fajl()

    print("\n" + "=" * 50)
    print("     REPÜLŐJEGY FOGLALÁSI RENDSZER")
    print("=" * 50)

    university_airline = LegiTarsasag("University Airline")

    j1 = BelfoldiJarat("UA001", "Budapest", 15000, 60)
    j2 = BelfoldiJarat("UA002", "Debrecen", 12000, 50)
    j3 = NemzetkoziJarat("UA003", "London", 65000, 180)

    university_airline.jarat_hozzaadas(j1)
    university_airline.jarat_hozzaadas(j2)
    university_airline.jarat_hozzaadas(j3)

    mai_datum = datetime.now().date()
    for i in range(6):
        jarat_idx = i % 3
        datum = mai_datum + timedelta(days=i + 1)

        jarat_obj = university_airline.jaratok[jarat_idx]
        foglalas = JegyFoglalas(str(uuid.uuid4())[:8], jarat_obj, datum)
        university_airline.foglalasok.append(foglalas)

    print(
        f"[INFO] Rendszer betöltve. {len(university_airline.jaratok)} járat és {len(university_airline.foglalasok)} előzetes foglalás betöltve.")

    while True:
        print("\nVálasszon műveletet:")
        print("1. Jegy foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")

        valasztas = input("Kérem adja meg a választása számát: ").strip()

        if valasztas == "1":
            university_airline.jaratok_listazasa()
            try:
                jarat_idx = int(input("Adja meg a járat számát: ")) - 1
                datum = input("Adja meg az utazás dátumát (ÉÉÉÉ-HH-NN): ")
                ar = university_airline.foglalas(jarat_idx, datum)
                if ar > 0:
                    print(f"-> A fizetendő összeg: {ar} Ft")
            except ValueError:
                print("[HIBA] Kérjük, számot adjon meg a járat kiválasztásához!")

        elif valasztas == "2":
            university_airline.foglalasok_listazasa()
            if len(university_airline.foglalasok) > 0:
                lemondando_id = input("Adja meg a lemondani kívánt foglalás ID-ját: ").strip()
                university_airline.lemondas(lemondando_id)

        elif valasztas == "3":
            university_airline.foglalasok_listazasa()

        elif valasztas == "4":
            print("Kilépés a rendszerből. Viszontlátásra!")
            break

        else:
            print("[HIBA] Érvénytelen menüpont. Kérjük, próbálja újra!")


if __name__ == "__main__":
    main()
