# Valutaomregner CLI

Et simpelt kommandolinje-program der omregner beløb mellem verdens valutaer ved hjælp af [exchangerate-api.com](https://www.exchangerate-api.com/).

---

## Kom i gang

### 1. Hent koden fra GitHub

```bash
git clone https://github.com/JuliusLyster/valuta-cli.git
cd valuta-cli
```

---

### 2. Opret virtuelt miljø

Et virtuelt miljø holder projektets pakker adskilt fra resten af din computer.

```bash
python3 -m venv venv
```

**Aktivér det:**

- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

Du kan se at det virker, fordi der nu står `(venv)` foran din prompt.

---

### 3. Installér afhængigheder

```bash
pip install -r requirements.txt
```

---

### 4. Hent en gratis API nøgle

Gå til [https://www.exchangerate-api.com/](https://www.exchangerate-api.com/), opret en gratis konto, og kopiér din API nøgle.

---

### 5. Kør programmet første gang

Angiv din API nøgle — den gemmes automatisk til `.env`, så du kun skal gøre det én gang:

```bash
python3 valuta.py --key DIN_API_NØGLE
```

---

## Brug

### Omregn et beløb

```bash
python3 valuta.py --from DKK --to USD --amount 100
```

```
 Valutaomregner
──────────────────────────────

  100,00 DKK
  = 14,23 USD

  Kurs: 1 DKK = 0.1423 USD
```

### Se alle tilgængelige valutaer

```bash
python3 valuta.py --list
```

### Brug en anden API nøgle (uden at gemme den)

```bash
python3 valuta.py --key NY_NØGLE --from EUR --to THB --amount 50
```

### Vis hjælp

```bash
python3 valuta.py --help
```

---

##  Deaktivér det virtuelle miljø

Når du er færdig:

```bash
deactivate
```

---

##  Projektstruktur

```
valuta-cli/
├── valuta.py          # Hovedprogrammet
├── requirements.txt   # Pakkeafhængigheder
├── .env.example       # Eksempel på .env fil
├── .gitignore         # Filer der ikke uploades til GitHub
└── README.md          # Denne fil
```

>  `.env` filen med din API nøgle uploades **ikke** til GitHub — det sørger `.gitignore` for.