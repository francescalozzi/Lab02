def carica_da_file(file_path):
    """Carica i libri dal file"""
    try:
        infile = open(file_path, 'r', encoding='utf-8')
        biblioteca = {}
        from csv import reader
        csv_reader = reader(infile)
        for row in csv_reader:
            if len(row) < 5:
                continue

            sezione = int(row[4])
            # creo il libro in precedenza in modo da usare strip() per eliminare eventuali spazi tra i titoli
            libro = {'nome_libro': row[0].strip(), 'autore': row[1].strip(), 'data': int(row[2]), 'pagine': int(row[3])}

            if sezione not in biblioteca:
                biblioteca[sezione] = [libro]
            else:
                biblioteca[sezione].append(libro)

        infile.close()
        return biblioteca

    except FileNotFoundError:
        print('Errore: file non trovato')
        return None


def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""

    if sezione not in biblioteca:
        print("Errore: sezione non esistente")
        return None

    for libro in biblioteca[sezione]:
        if libro["nome_libro"].lower() == titolo.lower():
            print("Errore: titolo già presente in questa sezione")
            return None

    nuovo_libro = {'nome_libro': titolo, 'autore': autore, 'data': anno, 'pagine': pagine}

    biblioteca[sezione].append(nuovo_libro)

    try:
        # con with non serve che venga scritta la chiusura del file
        with open(file_path, 'a', encoding='utf-8', newline='') as infile:
            import csv
            writer = csv.writer(infile)  # trasforma liste/tuple in righe CSV gestendo virgole, virgolette...

            print(
                file=infile),  # printa una riga vuota --> ci serve perchè sennò il primo libro aggiunto lo printerebbe sull'ultima riga dove c'è già un libro
            writer.writerow([titolo, autore, anno, pagine, sezione])

    # writer = csv.writer --> serve per scrivere righe nel file csv --> i dati vengono convertiti in formato csv
    except FileNotFoundError:
        print('Error: file not found')
        return None

    return nuovo_libro


def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""
    for sezione, libri in biblioteca.items():
        for libro in libri:
            if libro['nome_libro'].lower() == titolo.lower():
                return f'{libro['nome_libro']}, {libro['autore']}, {libro['data']}, {libro['pagine']}, {sezione}'
    return None


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    if sezione not in biblioteca:
        return None

    titoli = []
    for libro in biblioteca[sezione]:
        titoli.append(libro['nome_libro'])
    return sorted(titoli, key=str.lower)  # in questo modo se si aggiunge un titolo con la lettera maiuscola, lo rende minuscolo e c'è un ordinamento corretto


def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":