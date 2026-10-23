# Clásico Data 2026 — Les stats diront-elles la vérité ?

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MOSESCI/clasico-data-2026/blob/main/clasico_analyse.ipynb)

**FC Barcelone – Real Madrid · dimanche 25 octobre 2026 · 20h00 GMT · Spotify Camp Nou**
Une analyse de données ouverte par **Moïse Monnin, Data Analyst**.

> Analyse à but pédagogique — ceci n'est pas un conseil de pari.

## Ce que dit l'analyse

| Question | Réponse des données |
|---|---|
| Qui domine l'histoire ? | Personne : 264 Clásicos officiels, **106 victoires chacun**, 52 nuls |
| L'équipe la plus en forme gagne-t-elle ? | **11 fois sur 18** (61 %) — mais un pile ou face ferait aussi bien 1 fois sur 4 |
| La forme actuelle ? | **12/15 pour les deux**. Barça +9 de différence de buts, Real +7 |
| Le pronostic du modèle ? | **Barça 61 % · Nul 20 % · Real 19 %**, score le plus probable 2-1 |
| Et le marché ? | Barça 59 % · Nul 16 % · Real 24 % — les méthodes convergent |

## Lancer l'analyse

Le plus simple : cliquer sur le badge **Open in Colab** ci-dessus, puis exécuter les cellules une à une avec **Shift + Entrée**.
Rien à installer. Le notebook lit les données directement depuis ce dépôt.

## La méthode, expliquée simplement

### 1. Les données
- **595 matchs officiels** du Barça et du Real depuis l'été 2021 (Liga, Ligue des champions, Coupe du Roi, Supercoupes…).
- Chaque score vient d'**ESPN** et a été **comparé à Wikipédia** : 591 matchs présents dans les deux sources, **0 écart**.
  Les 4 restants sont des matchs très récents ou décalés d'un jour à cause du fuseau horaire.
- Pour chaque but, on connaît le **buteur et le passeur** (ESPN). Le total des buts détaillés correspond au score final de chaque match.
- Les **xG** (*expected goals*) viennent d'**Understat** et ne concernent que la Liga.

### 2. La « forme »
Points pris (victoire 3, nul 1, défaite 0) et différence de buts sur les **5 matchs officiels précédents**.
L'équipe « en meilleure forme » a plus de points ; à égalité, la meilleure différence de buts.

### 3. Les joueurs
Six attaquants titulaires probables : Lamine Yamal, Raphinha, Fermín López (Barça) ; Kylian Mbappé, Jude Bellingham, Arda Güler (Real).
Vinícius Júnior, suspendu, n'est pas suivi. Mesure : buts + passes décisives par match, uniquement sur les matchs où le joueur a joué.

### 4. Le modèle de Poisson
La loi de Poisson donne la probabilité qu'une équipe marque 0, 1, 2… buts quand on connaît sa moyenne attendue (λ).

- **Attaque** = buts marqués par match ÷ moyenne de la Liga ; **défense** = buts encaissés par match ÷ moyenne de la Liga.
- Calculées sur les **38 derniers matchs de Liga** de chaque club (9 matchs cette saison, c'est trop peu).
- λ Barça = attaque Barça × défense Real × moyenne des buts à domicile ; λ Real = attaque Real × défense Barça × moyenne à l'extérieur.
- On croise les probabilités de chaque score (0-0, 1-0, 2-1…) pour obtenir victoire / nul / défaite.
- **Vérification :** le même calcul avec les xG donne Barça 62 % · Nul 17 % · Real 21 %.

### 5. Le marché
Moyenne de 4 opérateurs (cotes agrégées par OddsJam, publiées par RotoWire le 21/10/2026), converties en probabilités,
marge retirée. Aucun opérateur n'est cité.

## Fiche de défense — questions qu'on peut te poser

**« Pourquoi Poisson et pas un modèle plus complexe ? »**
C'est le modèle de référence pour les scores de football : simple, explicable, et les résultats sont proches du marché.
Un modèle plus complexe sur si peu de données risquerait de « sur-apprendre ».

**« 18 matchs, ce n'est pas assez ! »**
Exactement — et c'est dit dans l'analyse. Avec 11 sur 18, la probabilité d'un tel score par pur hasard est de 24 %.
C'est une tendance, pas une preuve.

**« Tu ne tiens pas compte des absents ? »**
Non, et c'est une limite assumée : le modèle mesure la force collective récente. L'absence de Vinícius pourrait réduire
les chances du Real par rapport à ce qu'il affiche.

**« Pourquoi l'avantage du terrain ? »**
Il est intégré : on utilise la moyenne de buts à domicile pour le Barça et à l'extérieur pour le Real (Liga 2025-27).

**« Et si le Barça perd ? »**
Le modèle ne dit pas « le Barça va gagner », il dit « 61 % ». Un événement à 39 % arrive très souvent.
On mesurera lundi à quel point le résultat était surprenant.

## Organisation du dépôt

```
clasico_analyse.ipynb      le notebook (à ouvrir dans Colab)
data/                      les données propres, figées au 23/10/2026
  matchs.csv               matchs officiels + contrôle Wikipédia + xG
  buts.csv                 buteurs et passeurs
  presences.csv            présence des 6 joueurs suivis
  liga_2025_26.csv, liga_2026_27.csv   tous les matchs de Liga
  cotes.csv                cotes du marché (anonymisées)
graphiques/                graphiques exportés par le notebook
carrousel/                 carrousels LinkedIn (charte, générateurs, HTML, PDF, images)
collecte/                  scripts de collecte et de construction des données
```

### Reproduire la collecte (facultatif)
Les scripts de `collecte/` interrogent Wikipédia, ESPN et Understat avec des requêtes espacées.
`construire_donnees.py` assemble les fichiers bruts dans `data/`. `generer_notebook.py` régénère le notebook.

### Carrousel
Chaque club garde sa charte : rayures *blaugrana* et or pour le Barça, blanc, or et bleu marine pour le Real.
Les slides qui comparent les deux sont partagées en deux. Aucun blason ni logo officiel n'est utilisé.

- `carrousel/charte.css` : les couleurs et la mise en forme communes aux deux carrousels.
- `carrousel/generer_post1.py` : construit `post1_pronostic.html` à partir de `resultats.json` (aucun chiffre recopié à la main).
- `carrousel/generer_post2.py` : construit le gabarit `post2_verdict.html` ; les zones `[À REMPLIR]` se complètent après le match.
- `python carrousel/exporter.py carrousel/post1_pronostic.html` : produit le PDF et une image par slide (nécessite Chrome ou Edge).

## Sources
- Wikipédia : *List of El Clásico matches* et pages saison du FC Barcelona et du Real Madrid CF
- ESPN : résultats, buteurs, passeurs, compositions
- Understat : expected goals (Liga)
- RotoWire / OddsJam : cotes du 21/10/2026 ; presse sportive du 21 au 23/10/2026 pour les absences

---
Moïse Monnin · Data Analyst
