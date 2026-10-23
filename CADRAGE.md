# Clásico Data 2026 — Cahier des charges

**Auteur :** Moïse Monnin — Data Analyst
**Match :** FC Barcelone – Real Madrid, dimanche 25 octobre 2026, 20h00 GMT
**Question centrale :** les stats diront-elles la vérité ?

## Décisions

| Sujet | Décision |
|---|---|
| Livrable | Carrousel LinkedIn en 2 temps : pronostic (post n°1) puis verdict (post n°2) |
| Période | Bilan global depuis 1902 (accroche) + analyse fine sur les 15–20 derniers Clásicos, toutes compétitions |
| Forme équipe | Points + différence de buts sur les 5 matchs précédents (toutes compétitions) ; xG en bonus si disponibles |
| Forme joueurs | 6 attaquants titulaires probables (3 par club) : buts + passes décisives sur les 5 matchs avant le Clásico vs pendant le Clásico |
| Pronostic | Modèle de Poisson → probabilités V/N/D + score le plus probable ; 1 ligne « modèle vs marché » |
| Cotes | En probabilités implicites, moyenne de plusieurs sources, aucun bookmaker cité ; mention « Analyse pédagogique — pas un conseil de pari » |
| Outils | Python (notebook commenté en français), README pédagogique, badge « Open in Colab » |
| Exécution | Google Colab — Moïse s'approprie le notebook avant publication |
| Carrousel | PDF 1080 × 1350 prêt à publier + fichier source modifiable (HTML) |
| Identité | Moïse Monnin, Data Analyst ; charte sombre neutre ; couleurs clubs uniquement pour coder les données (grenat Barça, doré Real) |
| Langue | Tout en français |
| Fiabilité | Source principale FBref, contrôle Transfermarkt, vérification manuelle des chiffres affichés, sources citées sur chaque slide |
| GitHub | `MOSESCI/clasico-data-2026` (public) — aucune publication sans accord explicite |

## Calendrier (GMT)

- **Samedi 24 oct., 22h00** — carrousel n°1 finalisé et relu
- **Dimanche 25 oct., 11h00** — publication post n°1
- **Dimanche 25 oct., soir** — remplissage du carrousel n°2
- **Lundi 26 oct., 8h00** — publication post n°2

## Carrousel n°1 — 9 slides

1. Accroche — « Le Clásico de ce soir : les données ont-elles déjà le résultat ? »
2. Bilan historique depuis 1902
3. Méthode (échantillon, forme sur 5 matchs, Poisson)
4. Preuve n°1 — l'équipe la plus en forme gagne-t-elle ?
5. Forme actuelle Barça vs Real
6. Joueurs — forme avant vs rendement pendant le Clásico
7. Pronostic — probabilités V/N/D, score le plus probable, modèle vs marché
8. Limites — ce que les stats ne voient pas
9. Question ouverte + appel à commenter son pronostic

## Carrousel n°2 — 7 slides

1. Accroche — « J'avais donné X % au [favori]. Voici ce qui s'est passé. »
2. Résultat vs prédiction
3. Prédit vs réel (buts, xG, possession, tirs)
4. Les 6 joueurs suivis
5. Ce que le modèle a vu
6. Ce que le modèle n'a pas vu
7. La leçon — les stats ont-elles dit la vérité ?
