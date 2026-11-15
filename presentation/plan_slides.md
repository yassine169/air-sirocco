# Plan des slides (10 minutes, 9 slides)

| # | Slide | Qui parle | Contenu |
|---|---|---|---|
| 1 | Titre | Nadia | « Air & Sirocco », noms des 4 membres |
| 2 | Problématique | Nadia | Sirocco → poussière du Sahara → pollution → personnes fragiles ; pas de suivi fiable ville par ville. Exemple réel : **Sfax, 13 nov., 11h → PM10 = 90,7 µg/m³** (2× le seuil OMS de 45) |
| 3 | Sources | Nadia | Tableau des 3 sources ; pourquoi Open-Meteo (pas de clé, couvre la Tunisie) |
| 4 | Questions métier | Nadia | 1) Dépassements OMS par ville 2) Effet du vent du sud 3) Fiabilité des prévisions |
| 5 | Architecture | Nadia | Image `docs/architecture.png` ; une couleur = un membre |
| 6 | Ingestion | Yassine | Démo : lancer 2 fois, nombre de lignes identique ; contrat qui bloque |
| 7 | dbt | Youssef | Démo : `dbt build` vert ; table `fct_daily_exceedances` |
| 8 | CI & Docker | Fedi | Démo : PR rouge bloquée ; `docker compose up` |
| 9 | Santé + suite | Nadia | Démo `check_data.py` ; au-delà du cours : alerte avant l'épisode, série bloquée, page santé ; planning (Prefect, Discord, tableau de bord, AWS) |

Conseils :
- Une idée par slide, peu de texte, de grandes images.
- Préparer les démos à l'avance (terminal déjà ouvert, police agrandie).
- Avoir des captures d'écran de secours si Internet ne marche pas pendant la soutenance.

Captures de secours (annexe) :
- [ ] ingestion lancée 2 fois : 360 → 360 lignes
- [ ] `dbt build` tout vert
- [ ] PR rouge bloquée par la CI
- [ ] `python scripts/check_data.py` → ✅ Données fraîches et complètes
