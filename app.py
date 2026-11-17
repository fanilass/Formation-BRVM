"""
Application Éducative BRVM - Formation à la Bourse
===================================================
Cette application permet aux étudiants d'apprendre le fonctionnement
de la Bourse Régionale des Valeurs Mobilières (BRVM) de manière interactive.

Modules inclus:
1. Introduction à la BRVM
2. Concepts fondamentaux
3. Analyse technique et fondamentale
4. Simulation de trading
5. Quiz et évaluations
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Formation BRVM - Bourse Éducative",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# STYLES CSS PERSONNALISÉS
# ==========================================
st.markdown("""
<style>
    /* Styles pour les cartes d'information */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Styles pour les métriques */
    .metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }

    /* Titre principal */
    .main-title {
        font-size: 2.5em;
        color: #667eea;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Sous-titre */
    .subtitle {
        font-size: 1.2em;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Bouton personnalisé */
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 5px;
        padding: 10px 25px;
        border: none;
        font-weight: bold;
    }

    /* Zone de quiz */
    .quiz-question {
        background: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 5px solid #2196f3;
    }

    /* Succès */
    .success-box {
        background: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        color: #155724;
    }

    /* Erreur */
    .error-box {
        background: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# INITIALISATION DU STATE
# ==========================================
# Le state permet de conserver les données entre les rafraîchissements
if 'current_module' not in st.session_state:
    st.session_state.current_module = "Accueil"

if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0

if 'portfolio' not in st.session_state:
    # Portfolio de simulation de trading
    st.session_state.portfolio = {
        'cash': 1000000,  # 1 million FCFA
        'stocks': {},
        'history': []
    }

if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False

if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

# ==========================================
# DONNÉES ÉDUCATIVES SUR LA BRVM
# ==========================================

# Informations générales sur la BRVM
BRVM_INFO = {
    'nom_complet': 'Bourse Régionale des Valeurs Mobilières',
    'creation': '18 décembre 1996 à Cotonou, au Bénin.',
    'siege': 'Abidjan, Côte d\'Ivoire',
    'pays_membres': ['Bénin', 'Burkina Faso', 'Côte d\'Ivoire', 'Guinée-Bissau',
                     'Mali', 'Niger', 'Sénégal', 'Togo'],
    'devise': 'Franc CFA (XOF)',
    'indices': ['BRVM 10', 'BRVM Composite', 'BRVM Prestige'],
    'horaires': '09h00 - 15h00 (GMT)',
    'jours_cotation': 'Lundi au Vendredi'
}

# Lexique boursier complet - Concepts fondamentaux expliqués
CONCEPTS_FONDAMENTAUX = {
    # ===== TITRES ET INSTRUMENTS FINANCIERS =====
    'Action': {
        'definition': 'Une action représente une part du capital d\'une entreprise. '
                      'En achetant une action, vous devenez propriétaire d\'une partie de l\'entreprise (actionnaire).',
        'exemple': 'Si vous achetez 100 actions Sonatel à 10 000 FCFA l\'action, '
                   'vous investissez 1 000 000 FCFA et possédez une petite partie de Sonatel.',
        'avantages': ['Dividendes potentiels', 'Plus-values possibles', 'Droit de vote en AG'],
        'risques': ['Perte en capital', 'Volatilité élevée', 'Risque de faillite']
    },
    'Action ordinaire': {
        'definition': 'Type d\'action le plus courant donnant droit de vote aux assemblées générales '
                      'et droit aux dividendes (non prioritaire).',
        'exemple': 'Avec 1000 actions ordinaires Ecobank, vous votez en AG et recevez les dividendes '
                   'après paiement des actionnaires privilégiés.',
        'avantages': ['Droit de vote', 'Participation aux décisions', 'Dividendes variables'],
        'risques': ['Dividende non garanti', 'Dernier servi en cas de liquidation']
    },
    'Action de préférence': {
        'definition': 'Action privilégiée offrant un dividende prioritaire et souvent plus élevé, '
                      'mais sans droit de vote.',
        'exemple': 'Une action de préférence peut garantir 8% de dividende annuel avant toute distribution '
                   'aux actionnaires ordinaires.',
        'avantages': ['Dividende prioritaire', 'Revenu plus stable', 'Moins volatile'],
        'risques': ['Pas de droit de vote', 'Potentiel de plus-value limité']
    },
    'Obligation': {
        'definition': 'Titre de créance représentant un emprunt émis par une entreprise ou un État. '
                      'L\'émetteur s\'engage à rembourser le capital avec intérêts (coupons).',
        'exemple': 'Une obligation d\'État à 5 ans avec coupon de 6% : pour 100 000 FCFA, '
                   'vous recevez 6 000 FCFA/an pendant 5 ans, puis 100 000 FCFA à l\'échéance.',
        'avantages': ['Revenus réguliers (coupons)', 'Moins volatile', 'Priorité sur actionnaires'],
        'risques': ['Risque de défaut', 'Risque de taux d\'intérêt', 'Risque d\'inflation']
    },
    'Obligation convertible': {
        'definition': 'Obligation qui peut être convertie en actions de l\'entreprise émettrice '
                      'selon des conditions prédéfinies.',
        'exemple': 'Une obligation convertible à 100 000 FCFA peut être échangée contre 10 actions '
                   'si le cours dépasse 12 000 FCFA.',
        'avantages': ['Sécurité de l\'obligation', 'Potentiel de l\'action', 'Flexibilité'],
        'risques': ['Rendement plus faible', 'Dilution possible', 'Complexité']
    },
    'Bon de souscription': {
        'definition': 'Droit d\'acheter une action à un prix fixé d\'avance pendant une période donnée. '
                      'Instrument dérivé négociable.',
        'exemple': 'Un bon vous permet d\'acheter une action à 10 000 FCFA. Si le cours monte à 15 000 FCFA, '
                   'vous gagnez 5 000 FCFA par bon exercé.',
        'avantages': ['Effet de levier', 'Risque limité au prix du bon', 'Flexibilité'],
        'risques': ['Durée limitée', 'Peut expirer sans valeur', 'Volatilité']
    },

    # ===== ACTEURS ET INTERMÉDIAIRES =====
    'Courtier (SGI)': {
        'definition': 'Société de Gestion et d\'Intermédiation agréée qui exécute les ordres d\'achat '
                      'et vente de titres pour le compte des investisseurs.',
        'exemple': 'Pour acheter des actions à la BRVM, vous devez obligatoirement passer par une SGI '
                   'qui transmettra votre ordre au marché.',
        'avantages': ['Accès au marché', 'Conseil professionnel', 'Sécurité des transactions'],
        'risques': ['Frais de courtage', 'Dépendance', 'Conflits d\'intérêts possibles']
    },
    'Teneur de marché': {
        'definition': 'Intermédiaire qui s\'engage à acheter et vendre en permanence certaines valeurs '
                      'pour assurer la liquidité du marché.',
        'exemple': 'Un teneur de marché affiche toujours des prix d\'achat et vente pour SONATEL, '
                   'facilitant les transactions.',
        'avantages': ['Liquidité accrue', 'Spread réduit', 'Facilite les transactions'],
        'risques': ['Coût pour les émetteurs', 'Manipulation possible']
    },
    'Dépositaire central (DC/BR)': {
        'definition': 'Organisme qui conserve les titres de manière dématérialisée et enregistre '
                      'tous les mouvements de titres.',
        'exemple': 'Le DC/BR conserve électroniquement vos 100 actions Ecobank et enregistre '
                   'chaque achat ou vente.',
        'avantages': ['Sécurité', 'Rapidité', 'Traçabilité'],
        'risques': ['Risque informatique', 'Dépendance technologique']
    },

    # ===== INDICATEURS ET VALORISATION =====
    'Capitalisation boursière': {
        'definition': 'Valeur totale d\'une entreprise cotée, calculée en multipliant le nombre d\'actions '
                      'par le cours de l\'action.',
        'exemple': 'Si Sonatel a 10 millions d\'actions à 15 000 FCFA, sa capitalisation est '
                   '150 milliards FCFA.',
        'avantages': ['Mesure de taille', 'Comparaison facile', 'Indicateur de liquidité'],
        'risques': ['Volatilité', 'Ne reflète pas toujours la valeur réelle']
    },
    'PER (Price Earnings Ratio)': {
        'definition': 'Ratio Cours/Bénéfice mesurant combien d\'années de bénéfice il faut '
                      'pour récupérer le prix de l\'action. PER = Cours / Bénéfice par action.',
        'exemple': 'Si une action vaut 20 000 FCFA et le bénéfice par action est 2 000 FCFA, '
                   'le PER = 10 (il faut 10 ans de bénéfice).',
        'avantages': ['Comparaison entre sociétés', 'Indicateur de cherté', 'Facile à calculer'],
        'risques': ['Ne tient pas compte de la croissance', 'Varie selon les secteurs']
    },
    'Dividende': {
        'definition': 'Part des bénéfices distribuée aux actionnaires. Décidé en Assemblée Générale, '
                      'versé annuellement ou semestriellement.',
        'exemple': 'Si une entreprise verse 500 FCFA de dividende par action '
                   'et que vous en possédez 100, vous recevez 50 000 FCFA.',
        'avantages': ['Revenu passif', 'Signe de santé financière', 'Rendement régulier'],
        'risques': ['Non garanti', 'Peut être réduit ou supprimé', 'Fiscalité (IRF)']
    },
    'Rendement du dividende': {
        'definition': 'Ratio entre le dividende annuel et le cours de l\'action, exprimé en pourcentage. '
                      'Rendement = (Dividende / Cours) × 100.',
        'exemple': 'Action à 10 000 FCFA versant 600 FCFA de dividende = rendement de 6%.',
        'avantages': ['Compare revenus entre actions', 'Mesure rentabilité', 'Simple'],
        'risques': ['Dividende peut baisser', 'Cours peut chuter', 'Varie dans le temps']
    },
    'Valeur nominale': {
        'definition': 'Valeur faciale d\'une action inscrite dans les statuts de la société. '
                      'Montant du capital social divisé par le nombre d\'actions.',
        'exemple': 'Une société avec 10 millions FCFA de capital et 10 000 actions a une valeur nominale '
                   'de 1 000 FCFA par action.',
        'avantages': ['Base de calcul des droits', 'Fixe et stable', 'Référence juridique'],
        'risques': ['Différente du cours', 'Peu d\'utilité pratique']
    },
    'Valeur comptable': {
        'definition': 'Valeur de l\'action calculée à partir du bilan comptable. '
                      'Actif net / Nombre d\'actions.',
        'exemple': 'Si une entreprise a 100 milliards d\'actifs nets et 5 millions d\'actions, '
                   'la valeur comptable est 20 000 FCFA.',
        'avantages': ['Basée sur données réelles', 'Mesure valeur patrimoniale', 'Utile pour analyse'],
        'risques': ['Peut différer du cours', 'Dépend méthodes comptables', 'Statique']
    },

    # ===== TRANSACTIONS ET ORDRES =====
    'Plus-value': {
        'definition': 'Gain réalisé lors de la vente d\'une action à un prix supérieur au prix d\'achat. '
                      'Soumise à l\'impôt sur les plus-values.',
        'exemple': 'Achat à 10 000 FCFA, vente à 12 000 FCFA = 2 000 FCFA de plus-value '
                   'par action (soit +20%).',
        'avantages': ['Gains potentiellement élevés', 'Pas de limite', 'Multiplicateur de patrimoine'],
        'risques': ['Impôts (3% BRVM)', 'Timing difficile', 'Peut devenir moins-value']
    },
    'Moins-value': {
        'definition': 'Perte réalisée lors de la vente d\'une action à un prix inférieur au prix d\'achat. '
                      'Peut être déduite fiscalement des plus-values.',
        'exemple': 'Achat à 15 000 FCFA, vente à 12 000 FCFA = 3 000 FCFA de moins-value par action (-20%).',
        'avantages': ['Déduction fiscale possible', 'Apprentissage', 'Réallocation'],
        'risques': ['Perte de capital', 'Impact psychologique', 'Réduction patrimoine']
    },
    'Carnet d\'ordres': {
        'definition': 'Liste de tous les ordres d\'achat et de vente en attente d\'exécution, '
                      'classés par prix et heure.',
        'exemple': 'Le carnet montre 500 actions à vendre à 10 500 FCFA et 300 à acheter à 10 400 FCFA.',
        'avantages': ['Transparence du marché', 'Visualise offre/demande', 'Aide à la décision'],
        'risques': ['Peut être manipulé', 'Liquidité variable', 'Information partielle']
    },
    'Spread (Fourchette)': {
        'definition': 'Écart entre le meilleur prix d\'achat (demande) et le meilleur prix de vente (offre). '
                      'Indicateur de liquidité.',
        'exemple': 'Meilleure offre d\'achat: 10 400 FCFA, meilleure offre de vente: 10 600 FCFA = '
                   'spread de 200 FCFA (1,9%).',
        'avantages': ['Mesure liquidité', 'Coût visible', 'Compare valeurs'],
        'risques': ['Coût de transaction', 'Varie selon liquidité', 'Pénalise petits volumes']
    },
    'Liquidité': {
        'definition': 'Facilité avec laquelle un titre peut être acheté ou vendu rapidement '
                      'sans impacter significativement son prix.',
        'exemple': 'Sonatel est très liquide (milliers d\'échanges/jour) alors qu\'une petite valeur '
                   'peut avoir peu d\'acheteurs.',
        'avantages': ['Facilite transactions', 'Spread réduit', 'Prix plus stable'],
        'risques': ['Varie dans le temps', 'Dépend du volume', 'Peut disparaître en crise']
    },
    'Volume': {
        'definition': 'Nombre de titres échangés sur une période donnée (jour, semaine, mois). '
                      'Indicateur d\'activité et de liquidité.',
        'exemple': 'Si 10 000 actions Ecobank sont échangées aujourd\'hui, le volume du jour est 10 000.',
        'avantages': ['Confirme tendances', 'Mesure intérêt', 'Indicateur de liquidité'],
        'risques': ['Volume faible = illiquide', 'Peut être artificiel', 'Varie fortement']
    },

    # ===== MARCHÉ ET COTATION =====
    'Indice boursier': {
        'definition': 'Indicateur synthétique mesurant la performance d\'un ensemble d\'actions. '
                      'Calculé à partir d\'un panier de valeurs représentatives.',
        'exemple': 'Le BRVM Composite suit l\'évolution de toutes les actions cotées. '
                   'S\'il monte de 5%, le marché global progresse de 5%.',
        'avantages': ['Vision globale du marché', 'Référence pour comparaison', 'Baromètre économique'],
        'risques': ['Ne représente pas tout', 'Peut être biaisé', 'Composition variable']
    },
    'Cotation': {
        'definition': 'Processus de fixation du prix d\'une action en bourse par confrontation '
                      'de l\'offre et de la demande.',
        'exemple': 'La cotation de Sonatel a lieu de 10h à 15h à la BRVM, son cours fluctue '
                   'selon les transactions.',
        'avantages': ['Prix de marché équitable', 'Transparence', 'Liquidité'],
        'risques': ['Volatilité', 'Manipulation possible', 'Gaps']
    },
    'Fixing': {
        'definition': 'Méthode de cotation où le prix est fixé une ou deux fois par jour '
                      'en regroupant tous les ordres. Utilisé pour les titres peu liquides.',
        'exemple': 'Une petite action cote une fois par jour à 10h30, tous les ordres de la journée '
                   's\'exécutent à ce moment.',
        'avantages': ['Simplifie échanges', 'Adapté aux petites valeurs', 'Moins de volatilité'],
        'risques': ['Liquidité limitée', 'Flexibilité réduite', 'Peut manquer opportunités']
    },
    'Cotation en continu': {
        'definition': 'Méthode où les échanges se font en temps réel tout au long de la séance boursière. '
                      'Pour les valeurs les plus liquides.',
        'exemple': 'Sonatel se négocie en continu de 10h à 15h, le cours change à chaque transaction.',
        'avantages': ['Liquidité maximale', 'Prix en temps réel', 'Flexibilité'],
        'risques': ['Volatilité intraday', 'Nécessite surveillance', 'Coûts de transaction']
    },
    'Suspendre de cotation': {
        'definition': 'Arrêt temporaire des échanges sur un titre, décidé par les autorités '
                      'en cas d\'annonce importante ou mouvement anormal.',
        'exemple': 'Si Ecobank annonce une fusion majeure, la cotation peut être suspendue '
                   'pour permettre au marché de digérer l\'info.',
        'avantages': ['Protège investisseurs', 'Évite panique', 'Temps de réflexion'],
        'risques': ['Blocage temporaire', 'Incertitude', 'Peut annoncer mauvaises nouvelles']
    },
    'Marché primaire': {
        'definition': 'Marché de l\'émission de nouveaux titres. L\'entreprise lève des fonds '
                      'directement auprès des investisseurs (introduction en bourse, augmentation de capital).',
        'exemple': 'Lors d\'une IPO, une entreprise vend ses actions pour la première fois au public '
                   'à 5 000 FCFA pour lever 10 milliards FCFA.',
        'avantages': ['Financement direct', 'Prix d\'émission attractif', 'Accès nouvelles opportunités'],
        'risques': ['Informations limitées', 'Incertitude', 'Lock-up period possible']
    },
    'Marché secondaire': {
        'definition': 'Marché où s\'échangent les titres déjà émis entre investisseurs. '
                      'L\'entreprise ne reçoit pas d\'argent, seuls les investisseurs échangent.',
        'exemple': 'Vous achetez des actions Sonatel à un autre investisseur via la BRVM. '
                   'Sonatel ne reçoit rien de cette transaction.',
        'avantages': ['Liquidité', 'Prix de marché', 'Entrée/sortie facile'],
        'risques': ['Volatilité', 'Frais de transaction', 'Pas de lien direct avec entreprise']
    },
    'Introduction en bourse (IPO)': {
        'definition': 'Première admission d\'une entreprise à la cotation. Elle vend ses actions '
                      'au public pour la première fois.',
        'exemple': 'Une entreprise décide d\'entrer en bourse et vend 30% de son capital '
                   'au public à 8 000 FCFA par action.',
        'avantages': ['Levée de capitaux', 'Notoriété', 'Liquidité pour actionnaires'],
        'risques': ['Coûts élevés', 'Obligations de transparence', 'Dilution capital']
    },

    # ===== ANALYSE ET STRATÉGIE =====
    'Analyse fondamentale': {
        'definition': 'Méthode d\'évaluation basée sur l\'étude des fondamentaux de l\'entreprise '
                      '(bilans, résultats, secteur, management) pour déterminer la valeur intrinsèque.',
        'exemple': 'Analyser les comptes d\'Ecobank, sa croissance, sa rentabilité et son secteur '
                   'pour décider si l\'action est sous-évaluée.',
        'avantages': ['Vision long terme', 'Valeur réelle', 'Moins spéculatif'],
        'risques': ['Chronophage', 'Nécessite compétences', 'Timing difficile']
    },
    'Analyse technique': {
        'definition': 'Méthode d\'analyse basée sur l\'étude des graphiques de prix et volumes '
                      'pour anticiper les mouvements futurs.',
        'exemple': 'Observer que l\'action forme un double creux à 9 500 FCFA peut signaler '
                   'un retournement haussier.',
        'avantages': ['Timing d\'entrée/sortie', 'Signaux clairs', 'Applicable partout'],
        'risques': ['Subjectif', 'Faux signaux', 'Prophétie autoréalisatrice']
    },
    'Support': {
        'definition': 'Niveau de prix où la demande est suffisamment forte pour empêcher '
                      'une nouvelle baisse. Zone d\'achat psychologique.',
        'exemple': 'Une action qui rebondit plusieurs fois sur 10 000 FCFA a un support à ce niveau.',
        'avantages': ['Point d\'entrée', 'Stop loss naturel', 'Repère psychologique'],
        'risques': ['Peut être cassé', 'Subjectif', 'Faux signaux']
    },
    'Résistance': {
        'definition': 'Niveau de prix où l\'offre est suffisamment forte pour empêcher '
                      'une nouvelle hausse. Zone de vente psychologique.',
        'exemple': 'Une action qui plafonne toujours à 15 000 FCFA a une résistance à ce niveau.',
        'avantages': ['Point de sortie', 'Target naturel', 'Repère important'],
        'risques': ['Peut être cassée', 'Auto-réalisation', 'Volatilité']
    },
    'Tendance': {
        'definition': 'Direction générale du mouvement des prix sur une période donnée. '
                      'Peut être haussière, baissière ou latérale.',
        'exemple': 'Si une action passe de 8 000 à 10 000 puis 12 000 FCFA sur 6 mois, '
                   'la tendance est haussière.',
        'avantages': ['Guide décisions', 'Probabilités', 'Simplifie vision'],
        'risques': ['Peut changer brutalement', 'Identification subjective', 'Retard']
    },
    'Volatilité': {
        'definition': 'Ampleur des variations de prix d\'un titre sur une période. '
                      'Mesure du risque et de l\'incertitude.',
        'exemple': 'Une action qui varie de ±10% par jour est très volatile, une autre à ±1% est stable.',
        'avantages': ['Opportunités de gains', 'Indicateur de risque', 'Utile pour options'],
        'risques': ['Pertes rapides', 'Stress', 'Difficile à prévoir']
    },
    'Bull Market (Marché haussier)': {
        'definition': 'Période prolongée où les cours boursiers augmentent de manière générale. '
                      'Optimisme et confiance dominent.',
        'exemple': 'De 2016 à 2019, la BRVM a connu un bull market avec +40% de hausse.',
        'avantages': ['Gains faciles', 'Moral positif', 'Accès facilité au crédit'],
        'risques': ['Euphorie irrationnelle', 'Valorisations excessives', 'Correction brutale']
    },
    'Bear Market (Marché baissier)': {
        'definition': 'Période prolongée de baisse généralisée des cours. Pessimisme et peur dominent.',
        'exemple': 'En 2020 avec le COVID, les marchés ont chuté de 30% en quelques semaines.',
        'avantages': ['Opportunités d\'achat', 'Valorisations attractives', 'Sélection naturelle'],
        'risques': ['Pertes importantes', 'Moral négatif', 'Liquidité réduite']
    },

    # ===== RISQUES ET GESTION =====
    'Diversification': {
        'definition': 'Stratégie consistant à répartir ses investissements sur plusieurs actifs '
                      'différents pour réduire le risque global.',
        'exemple': 'Au lieu d\'investir 1M FCFA dans une seule action, investir 200K dans 5 actions '
                   'de secteurs différents.',
        'avantages': ['Réduit risque spécifique', 'Lisse performance', 'Sommeil tranquille'],
        'risques': ['Dilue gains potentiels', 'Plus complexe', 'Coûts multiples']
    },
    'Stop loss': {
        'definition': 'Ordre automatique de vente déclenché si le cours atteint un seuil prédéfini. '
                      'Outil de gestion du risque.',
        'exemple': 'Vous achetez à 10 000 FCFA et placez un stop loss à 9 000 FCFA pour limiter '
                   'votre perte à 10%.',
        'avantages': ['Limite pertes', 'Automatique', 'Discipline'],
        'risques': ['Peut être déclenché par volatilité', 'Pas de retour', 'Timing']
    },
    'Risque systématique': {
        'definition': 'Risque affectant l\'ensemble du marché, non diversifiable. '
                      'Lié à l\'économie, politique, catastrophes.',
        'exemple': 'Une crise économique mondiale fait baisser toutes les actions, '
                   'même les meilleures.',
        'avantages': ['Impossible à éliminer', 'Affecte tous', 'Mesurable (bêta)'],
        'risques': ['Non diversifiable', 'Imprévisible', 'Peut être violent']
    },
    'Risque spécifique': {
        'definition': 'Risque propre à une entreprise ou secteur, diversifiable. '
                      'Lié à la gestion, concurrence, réglementation.',
        'exemple': 'Un scandale chez Ecobank fait chuter son action mais n\'affecte pas Sonatel.',
        'avantages': ['Diversifiable', 'Contrôlable partiellement', 'Analysable'],
        'risques': ['Nécessite diversification', 'Peut être soudain', 'Information asymétrique']
    }
}

# Types d'ordres de bourse
TYPES_ORDRES = {
    'Ordre au marché': 'Exécuté immédiatement au meilleur prix disponible',
    'Ordre à cours limité': 'Exécuté uniquement si le prix atteint votre limite',
    'Ordre à seuil de déclenchement': 'Devient actif quand un seuil est atteint',
    'Ordre à plage de déclenchement': 'Combinaison de limite et seuil'
}

# Stratégies d'investissement
STRATEGIES = {
    'Buy and Hold': {
        'description': 'Acheter et conserver à long terme (5+ ans)',
        'profil': 'Investisseurs patients, vision long terme',
        'avantages': 'Moins de stress, frais réduits, fiscalité avantageuse',
        'inconvenients': 'Nécessite patience, capital immobilisé'
    },
    'Day Trading': {
        'description': 'Achats et ventes dans la même journée',
        'profil': 'Traders actifs, temps disponible',
        'avantages': 'Profits rapides possibles, pas de risque overnight',
        'inconvenients': 'Très risqué, stressant, frais élevés'
    },
    'Swing Trading': {
        'description': 'Positions de quelques jours à quelques semaines',
        'profil': 'Traders intermédiaires',
        'avantages': 'Équilibre temps/rendement, profite des tendances',
        'inconvenients': 'Risque de gaps, nécessite analyse'
    },
    'Investissement de valeur': {
        'description': 'Acheter des actions sous-évaluées',
        'profil': 'Analystes fondamentaux',
        'avantages': 'Marge de sécurité, potentiel élevé',
        'inconvenients': 'Recherche intensive, patience requise'
    }
}

# ==========================================
# DONNÉES DE SIMULATION
# ==========================================

# Liste d'actions fictives inspirées de la BRVM
ACTIONS_BRVM = {
    'SONATEL': {'prix': 15000, 'secteur': 'Télécommunications', 'volatilite': 0.02},
    'ECOBANK': {'prix': 8500, 'secteur': 'Finance', 'volatilite': 0.025},
    'SAPHIR': {'prix': 12000, 'secteur': 'Industrie', 'volatilite': 0.03},
    'PALMCI': {'prix': 6500, 'secteur': 'Agroalimentaire', 'volatilite': 0.022},
    'CIE': {'prix': 2000, 'secteur': 'Énergie', 'volatilite': 0.018},
    'NESTLE': {'prix': 7800, 'secteur': 'Agroalimentaire', 'volatilite': 0.015},
    'ONTBF': {'prix': 4500, 'secteur': 'Transport', 'volatilite': 0.028},
    'SAFCA': {'prix': 950, 'secteur': 'Immobilier', 'volatilite': 0.032}
}


# ==========================================
# FONCTIONS UTILITAIRES
# ==========================================

def generer_historique_prix(action, jours=90):
    """
    Génère un historique de prix simulé pour une action

    Args:
        action: Nom de l'action
        jours: Nombre de jours d'historique

    Returns:
        DataFrame avec les prix historiques
    """
    prix_initial = ACTIONS_BRVM[action]['prix']
    volatilite = ACTIONS_BRVM[action]['volatilite']

    dates = [datetime.now() - timedelta(days=x) for x in range(jours, 0, -1)]

    # Simulation d'un mouvement brownien géométrique
    prix = [prix_initial]
    for i in range(1, jours):
        # Variation aléatoire basée sur la volatilité
        variation = np.random.normal(0, volatilite)
        nouveau_prix = prix[-1] * (1 + variation)
        prix.append(max(nouveau_prix, prix_initial * 0.5))  # Prix minimum à 50% du prix initial

    df = pd.DataFrame({
        'Date': dates,
        'Prix': prix,
        'Volume': np.random.randint(1000, 50000, jours)
    })

    return df


def calculer_indicateurs_techniques(df):
    """
    Calcule les indicateurs techniques sur un DataFrame de prix

    Args:
        df: DataFrame avec colonnes Date et Prix

    Returns:
        DataFrame enrichi avec indicateurs
    """
    # Moyenne mobile simple (SMA) sur 20 jours
    df['SMA_20'] = df['Prix'].rolling(window=20).mean()

    # Moyenne mobile simple sur 50 jours
    df['SMA_50'] = df['Prix'].rolling(window=50).mean()

    # RSI (Relative Strength Index)
    delta = df['Prix'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df


def afficher_graphique_chandelier(df, titre):
    """
    Affiche un graphique en chandelier japonais

    Args:
        df: DataFrame avec données OHLC
        titre: Titre du graphique
    """
    # Calcul des données OHLC simplifiées
    df['Open'] = df['Prix'].shift(1).fillna(df['Prix'])
    df['High'] = df[['Prix', 'Open']].max(axis=1) * 1.005
    df['Low'] = df[['Prix', 'Open']].min(axis=1) * 0.995
    df['Close'] = df['Prix']

    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Prix'
    )])

    fig.update_layout(
        title=titre,
        yaxis_title='Prix (FCFA)',
        xaxis_title='Date',
        template='plotly_white',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# MODULES DE L'APPLICATION
# ==========================================

def page_accueil():
    """
    Page d'accueil de l'application
    Présente l'application et guide l'utilisateur
    """
    # Titre principal avec HTML personnalisé
    st.markdown('<div class="main-title">🎓 Plateforme Éducative BRVM</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Maîtrisez la Bourse Régionale des Valeurs Mobilières</div>',
                unsafe_allow_html=True)

    # Image d'en-tête (bannière)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://via.placeholder.com/800x300/667eea/ffffff?text=BRVM+Formation",
                 use_column_width=True)

    st.markdown("---")

    # Présentation en colonnes
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🎯 Objectifs de la formation

        Cette plateforme vous permet de :

        - 📚 **Apprendre** les concepts fondamentaux de la bourse
        - 📊 **Comprendre** le fonctionnement de la BRVM
        - 💹 **Pratiquer** avec un simulateur de trading
        - 📈 **Analyser** les graphiques et indicateurs techniques
        - ✅ **Évaluer** vos connaissances avec des quiz
        """)

        # Statistiques de la BRVM
        st.markdown("### 📍 Informations BRVM")
        st.info(f"""
        **Siège**: {BRVM_INFO['siege']}  
        **Création**: {BRVM_INFO['creation']}  
        **Pays membres**: {len(BRVM_INFO['pays_membres'])} pays  
        **Devise**: {BRVM_INFO['devise']}
        """)

    with col2:
        st.markdown("### 📖 Modules disponibles")

        # Liste des modules avec icônes
        modules = [
            ("🏛️", "Introduction BRVM", "Découvrez l'histoire et le rôle de la BRVM"),
            ("📚", "Concepts Fondamentaux", "Maîtrisez les bases: actions, obligations, indices"),
            ("📊", "Analyse Technique", "Apprenez à lire les graphiques et indicateurs"),
            ("💰", "Simulateur Trading", "Pratiquez sans risque avec 1M FCFA virtuel"),
            ("🎯", "Quiz & Évaluation", "Testez vos connaissances")
        ]

        for icone, titre, description in modules:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{icone} {titre}</h4>
                <p style="margin:0; color:#666;">{description}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Pays membres avec drapeaux
    st.markdown("### 🌍 Pays membres de l'UEMOA")
    cols = st.columns(4)
    for idx, pays in enumerate(BRVM_INFO['pays_membres']):
        with cols[idx % 4]:
            st.markdown(f"🏴 **{pays}**")

    st.markdown("---")

    # Call to action
    st.markdown("""
    <div class="info-card">
        <h3 style="margin-top:0;">🚀 Commencez votre formation maintenant !</h3>
        <p>Utilisez le menu latéral pour naviguer entre les différents modules.</p>
        <p>💡 <strong>Conseil</strong>: Suivez les modules dans l'ordre pour une progression optimale.</p>
    </div>
    """, unsafe_allow_html=True)


def page_introduction():
    """
    Module d'introduction à la BRVM
    Présente l'histoire, le rôle et le fonctionnement
    """
    st.title("🏛️ Introduction à la BRVM")

    # Tabs pour organiser le contenu
    tab1, tab2, tab3, tab4 = st.tabs([
        "📜 Histoire",
        "🎯 Rôle et Mission",
        "⚙️ Fonctionnement",
        "📊 Chiffres Clés"
    ])

    with tab1:
        st.markdown("### 📜 Histoire de la BRVM")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            La **Bourse Régionale des Valeurs Mobilières (BRVM)** a été créée en **1996** 
            dans le cadre de l'intégration économique de l'Union Économique et Monétaire 
            Ouest Africaine (UEMOA).

            #### 🎯 Contexte de création

            La création de la BRVM est à la fois un succès politique, 
            économique, institutionnel et technique. Il s’agit de la seule 
            Bourse totalement intégrée au monde appartenant à plusieurs pays. 

            La création de la BRVM visait à :

            - ✅ Créer un Marché Financier Régional intégré pour 8 pays de l'UEMOA
            - ✅ Mobiliser l’épargne pour financer les économies de l’Union
            - ✅ Faciliter l’accès au financement par le marché des capitaux
            - ✅ Stimuler les investissements et les flux de capitaux dans l’Union
            - ✅ Moderniser les infrastructures financières régionales
            - ✅ Renforcer l'intégration économique et financière des États membres

            #### 📅 Dates clés

            - **1996**: Création juridique de la BRVM et du DC/BR 
            - **1998**: Démarrage officiel des activités de la BRVM et du DC/BR 
            - **1999**: Lancement de la cotation électronique décentralisée
            - **2000**: Extension progressive aux 8 pays
            - **2001**: Passage à la cotation quotidienne
            - **2013**: Passage à la cotation en continu
            - **2018**: Ouverture du troisième compartiment 
            """)

        with col2:
            st.image("https://via.placeholder.com/300x400/764ba2/ffffff?text=BRVM -+30 ans",
                     use_column_width=True)

            st.info("""
            **Le saviez-vous ?**

            La BRVM est l'une des rares bourses régionales au monde, permettant à 8 pays 
            de partager une même infrastructure boursière.
            """)

    with tab2:
        st.markdown("### 🎯 Rôle et Mission de la BRVM")

        st.markdown("""
        La BRVM joue plusieurs rôles essentiels dans l'économie de la zone UEMOA :
        """)

        # Cartes de rôles
        roles = [
            {
                'titre': '💼 Financement des entreprises',
                'description': 'Permet aux entreprises de lever des fonds pour leur développement '
                               'en émettant des actions ou obligations.',
                'exemple': 'Une entreprise peut lever 5 milliards FCFA en émettant des actions '
                           'plutôt que de s\'endetter auprès des banques.'
            },
            {
                'titre': '💰 Placement pour investisseurs',
                'description': 'Offre aux particuliers et institutions un canal d\'investissement '
                               'pour faire fructifier leur épargne.',
                'exemple': 'Un épargnant peut investir dans Sonatel et recevoir des dividendes '
                           'chaque année.'
            },
            {
                'titre': '📊 Transparence et régulation',
                'description': 'Garantit la transparence des transactions et protège les investisseurs '
                               'grâce à des règles strictes.',
                'exemple': 'Toutes les sociétés cotées doivent publier leurs résultats financiers '
                           'régulièrement.'
            },
            {
                'titre': '🌍 Intégration régionale',
                'description': 'Favorise l\'intégration économique et la libre circulation des capitaux '
                               'dans l\'UEMOA.',
                'exemple': 'Un investisseur sénégalais peut facilement acheter des actions d\'une '
                           'entreprise ivoirienne.'
            }
        ]

        for role in roles:
            with st.expander(f"**{role['titre']}**", expanded=True):
                st.markdown(f"{role['description']}")
                st.success(f"**Exemple concret**: {role['exemple']}")

    with tab3:
        st.markdown("### ⚙️ Fonctionnement de la BRVM")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            #### 🕐 Horaires de cotation
            """)
            st.info(f"""
            **Jours**: {BRVM_INFO['jours_cotation']}  
            **Horaires**: {BRVM_INFO['horaires']}

            **Phases de négociation**:
            - 09h45 - 09h45 : Pré-ouverture
            - 09h45 - 14h00 : Négociation en continu
            - 14h00 - 14h30 : Pré-clôture
            - 14h30: Fixing de clôture
            - 14h30 - 15h00 : Négociation au dernier cours
            - 15h00 : Fermeture et officialisation du marché
            """)

            st.markdown("""
            #### 💻 Système de cotation

            La BRVM utilise un système de **cotation électronique** moderne qui permet :

            - ⚡ Des transactions rapides et sécurisées
            - 📱 L'accès à distance pour les courtiers
            - 🔄 La transparence en temps réel
            - 📊 L'enregistrement automatique
            """)

        with col2:
            st.markdown("""
            #### 👥 Acteurs du marché
            """)

            acteurs = {
                '🏢 Sociétés cotées': 'Entreprises qui émettent des titres',
                '💼 Investisseurs': 'Acheteurs et vendeurs de titres',
                '🏦 SGI (Société de Gestion et d’Intermédiation)': 'Intermédiaires agréés',
                '👨‍⚖️ AMF-UMOA': 'Régulateur du marché',
                '🏛️ DC/BR (Dépositaire Central/Banque de Règlement)': 'Conservation des titres',
                '📊 BRVM': 'Organise les cotations'
            }

            for acteur, role in acteurs.items():
                st.markdown(f"**{acteur}**  \n{role}")
                st.markdown("")

            st.warning("""
            **Important**: Vous ne pouvez pas acheter directement en bourse. 
            Vous devez passer par une SGI (Société de Gestion et d'Intermédiation) agréée.
            """)

    with tab4:
        st.markdown("### 📊 Chiffres Clés de la BRVM")

        # Métriques simulées (à titre éducatif)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Sociétés cotées",
                value="48",
                delta="Actions"
            )

        with col2:
            st.metric(
                label="Capitalisation actions",
                value="20 351 Mds",
                delta="FCFA"
            )

        with col2:
            st.metric(
                label="Capitalisation obligations",
                value="13 434 Mds",
                delta="FCFA"
            )


        with col3:
            st.metric(
                label="Indices",
                value="3",
                delta="Principaux"
            )

        with col3:
            st.metric(
                label="SGI",
                value="36"
                    )

        with col4:
            st.metric(
                label="Pays",
                value="8",
                delta="UEMOA"
            )

        st.markdown("---")

        # Graphique de répartition par secteur (simulation)
        st.markdown("#### 📈 Répartition par secteur")

        secteurs_data = {
            'Secteur': ['Finance', 'Industrie', 'Agriculture', 'Distribution',
                        'Services publics', 'Transport', 'Autres'],
            'Nombre': [12, 8, 6, 5, 4, 3, 7]
        }
        df_secteurs = pd.DataFrame(secteurs_data)

        fig = px.pie(df_secteurs, values='Nombre', names='Secteur',
                     title='Répartition des sociétés cotées par secteur',
                     color_discrete_sequence=px.colors.sequential.Purples)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Indices de la BRVM
        st.markdown("#### 📊 Les Indices de la BRVM")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>BRVM Composite</h4>
                <p>Mesure l'évolution globale de l'ensemble des sociétés cotées à la BRVM </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>BRVM 30</h4>
                <p>Regroupe les 30 valeurs les plus échangées sur le marché, selon leur liquidité</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>BRVM Prestige</h4>
                <p>Regroupe les sociétés cotées sur le compartiment Prestige</p>
            </div>
            """, unsafe_allow_html=True)

        with col1:
            st.markdown("""
                  <div class="metric-card">
                      <h4>BRVM Principal</h4>
                      <p>Suit les valeurs inscrites au compartiment Principal</p>
                  </div>
                  """, unsafe_allow_html=True)


def page_concepts_fondamentaux():
    """
    Module des concepts fondamentaux de la bourse
    Explique actions, obligations, dividendes, etc.
    """
    st.title("📚 Lexique Boursier Complet")

    st.markdown("""
    Bienvenue dans le lexique complet de la bourse ! Plus de **50 termes financiers** 
    expliqués avec des exemples concrets adaptés à la BRVM.
    """)

    # Tabs pour organiser le contenu
    tab1, tab2, tab3 = st.tabs(["🔍 Recherche par terme", "📑 Par catégorie", "🔤 Index alphabétique"])

    with tab1:
        st.markdown("### 🔍 Recherche de termes")

        # Barre de recherche
        recherche = st.text_input(
            "Entrez un terme à rechercher:",
            placeholder="Ex: action, dividende, PER...",
            key="recherche_terme"
        )

        if recherche:
            # Filtrer les concepts correspondants
            concepts_trouves = {
                k: v for k, v in CONCEPTS_FONDAMENTAUX.items()
                if recherche.lower() in k.lower() or
                   recherche.lower() in v['definition'].lower()
            }

            if concepts_trouves:
                st.success(f"✅ {len(concepts_trouves)} résultat(s) trouvé(s)")

                for terme, infos in concepts_trouves.items():
                    with st.expander(f"**{terme}**", expanded=True):
                        st.markdown(f"**📖 Définition:** {infos['definition']}")
                        st.info(f"**💡 Exemple:** {infos['exemple']}")

                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown("**✅ Avantages:**")
                            for av in infos['avantages']:
                                st.markdown(f"- {av}")
                        with col_b:
                            st.markdown("**⚠️ Risques:**")
                            for rq in infos['risques']:
                                st.markdown(f"- {rq}")
            else:
                st.warning("❌ Aucun résultat trouvé. Essayez un autre terme.")
        else:
            st.info("💡 Commencez à taper pour rechercher un terme boursier")

        st.markdown("---")

        # Sélection du concept via selectbox
        st.markdown("### 📚 Ou sélectionnez directement un terme:")

        concept_selectionne = st.selectbox(
            "Choisissez un concept à approfondir:",
            options=list(CONCEPTS_FONDAMENTAUX.keys()),
            key="concept_select_tab1"
        )

        st.markdown("---")

        # Affichage du concept sélectionné
        concept = CONCEPTS_FONDAMENTAUX[concept_selectionne]

        col1, col2 = st.columns([2, 1])

        with col1:
            # Définition
            st.markdown(f"### 📖 {concept_selectionne}")
            st.markdown(concept['definition'])

            st.markdown("---")

            # Exemple pratique
            st.markdown("### 💡 Exemple Pratique")
            st.success(concept['exemple'])

            st.markdown("---")

            # Avantages et risques en colonnes
            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("### ✅ Avantages")
                for avantage in concept['avantages']:
                    st.markdown(f"- {avantage}")

            with col_b:
                st.markdown("### ⚠️ Risques")
                for risque in concept['risques']:
                    st.markdown(f"- {risque}")

        with col2:
            # Illustration visuelle (placeholder)
            st.image(f"https://via.placeholder.com/400x300/667eea/ffffff?text={concept_selectionne.replace(' ', '+')}",
                     use_column_width=True)

            # Conseil pratique
            st.info("""
            **💡 Conseil pour débutants**

            Avant d'investir, assurez-vous de bien comprendre 
            tous ces concepts. N'hésitez pas à utiliser le 
            simulateur de trading pour pratiquer sans risque !
            """)

    with tab2:
        st.markdown("### 📑 Concepts par Catégorie")

        # Organisation par catégories
        categories = {
            "💼 Titres et Instruments": [
                "Action", "Action ordinaire", "Action de préférence",
                "Obligation", "Obligation convertible", "Bon de souscription"
            ],
            "👥 Acteurs du Marché": [
                "Courtier (SGI)", "Teneur de marché", "Dépositaire central (DC/BR)"
            ],
            "📊 Indicateurs et Valorisation": [
                "Capitalisation boursière", "PER (Price Earnings Ratio)",
                "Dividende", "Rendement du dividende", "Valeur nominale", "Valeur comptable"
            ],
            "💰 Transactions et Ordres": [
                "Plus-value", "Moins-value", "Carnet d'ordres",
                "Spread (Fourchette)", "Liquidité", "Volume"
            ],
            "📈 Marché et Cotation": [
                "Indice boursier", "Cotation", "Fixing", "Cotation en continu",
                "Suspendre de cotation", "Marché primaire", "Marché secondaire",
                "Introduction en bourse (IPO)"
            ],
            "🔍 Analyse et Stratégie": [
                "Analyse fondamentale", "Analyse technique", "Support",
                "Résistance", "Tendance", "Volatilité",
                "Bull Market (Marché haussier)", "Bear Market (Marché baissier)"
            ],
            "⚠️ Risques et Gestion": [
                "Diversification", "Stop loss", "Risque systématique", "Risque spécifique"
            ]
        }

        categorie_selectionnee = st.selectbox(
            "Choisissez une catégorie:",
            options=list(categories.keys()),
            key="categorie_select"
        )

        st.markdown(f"#### {categorie_selectionnee}")

        # Affichage des termes de la catégorie
        for terme in categories[categorie_selectionnee]:
            if terme in CONCEPTS_FONDAMENTAUX:
                with st.expander(f"**{terme}**"):
                    concept = CONCEPTS_FONDAMENTAUX[terme]
                    st.markdown(f"**Définition:** {concept['definition']}")
                    st.info(f"**Exemple:** {concept['exemple']}")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**✅ Avantages:**")
                        for av in concept['avantages']:
                            st.markdown(f"- {av}")
                    with col2:
                        st.markdown("**⚠️ Risques:**")
                        for rq in concept['risques']:
                            st.markdown(f"- {rq}")

    with tab3:
        st.markdown("### 🔤 Index Alphabétique")

        st.markdown("""
        Tous les termes du lexique classés par ordre alphabétique. 
        Cliquez sur un terme pour voir sa définition complète.
        """)

        # Tri alphabétique
        termes_alphabetiques = sorted(CONCEPTS_FONDAMENTAUX.keys())

        # Organisation en colonnes pour un affichage compact
        col1, col2, col3 = st.columns(3)

        # Répartition des termes sur 3 colonnes
        nb_termes_par_col = len(termes_alphabetiques) // 3 + 1

        with col1:
            for terme in termes_alphabetiques[:nb_termes_par_col]:
                with st.expander(f"**{terme}**"):
                    concept = CONCEPTS_FONDAMENTAUX[terme]
                    st.markdown(f"{concept['definition'][:150]}...")
                    if st.button(f"Voir détails", key=f"detail_{terme}_1"):
                        st.info(f"**Exemple:** {concept['exemple']}")

        with col2:
            for terme in termes_alphabetiques[nb_termes_par_col:nb_termes_par_col * 2]:
                with st.expander(f"**{terme}**"):
                    concept = CONCEPTS_FONDAMENTAUX[terme]
                    st.markdown(f"{concept['definition'][:150]}...")
                    if st.button(f"Voir détails", key=f"detail_{terme}_2"):
                        st.info(f"**Exemple:** {concept['exemple']}")

        with col3:
            for terme in termes_alphabetiques[nb_termes_par_col * 2:]:
                with st.expander(f"**{terme}**"):
                    concept = CONCEPTS_FONDAMENTAUX[terme]
                    st.markdown(f"{concept['definition'][:150]}...")
                    if st.button(f"Voir détails", key=f"detail_{terme}_3"):
                        st.info(f"**Exemple:** {concept['exemple']}")

    st.markdown("---")

    # Section informations complémentaires
    st.markdown("### 📚 Ressources Complémentaires")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 📝 Types d'ordres de bourse

        Pour acheter ou vendre des actions, vous devez passer un **ordre de bourse**. 
        Voici les principaux types :
        """)

        for type_ordre, description in TYPES_ORDRES.items():
            with st.expander(f"**{type_ordre}**"):
                st.markdown(description)

                # Exemples pour chaque type
                if type_ordre == 'Ordre au marché':
                    st.info("""
                    **Exemple**: Vous voulez acheter Sonatel immédiatement. 
                    Vous passez un ordre au marché et achetez au prix actuel (ex: 15 000 FCFA).
                    """)
                elif type_ordre == 'Ordre à cours limité':
                    st.info("""
                    **Exemple**: Sonatel est à 15 000 FCFA mais vous voulez acheter à 14 500 FCFA maximum. 
                    Votre ordre ne s'exécute que si le prix descend à 14 500 FCFA ou moins.
                    """)

    with col2:
        st.markdown("""
        #### 🎯 Stratégies d'Investissement

        Découvrez les différentes approches pour investir en bourse :
        """)

        strategie_selectionnee = st.selectbox(
            "Choisissez une stratégie à découvrir:",
            options=list(STRATEGIES.keys()),
            key="strategie_select_concepts"
        )

        strategie = STRATEGIES[strategie_selectionnee]

        st.markdown(f"**{strategie_selectionnee}**")
        st.markdown(f"{strategie['description']}")
        st.markdown(f"**Profil**: {strategie['profil']}")

        col_av, col_inc = st.columns(2)
        with col_av:
            st.markdown("**✅ Avantages**")
            st.markdown(strategie['avantages'])
        with col_inc:
            st.markdown("**⚠️ Inconvénients**")
            st.markdown(strategie['inconvenients'])

    st.markdown("---")

    # Statistiques du lexique
    st.markdown("### 📊 Statistiques du Lexique")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Termes", len(CONCEPTS_FONDAMENTAUX))

    with col2:
        st.metric("Catégories", "7")

    with col3:
        st.metric("Exemples Concrets", len(CONCEPTS_FONDAMENTAUX))

    with col4:
        st.metric("Couverture", "100%")

    st.success("""
    💡 **Conseil d'utilisation**: Consultez régulièrement ce lexique pendant votre apprentissage. 
    Chaque terme est expliqué avec des exemples concrets adaptés au contexte de la BRVM.
    """)


def page_analyse_technique():
    """
    Module d'analyse technique
    Présente les graphiques, indicateurs et outils d'analyse
    """
    st.title("📊 Analyse Technique")

    st.markdown("""
    L'analyse technique consiste à étudier les graphiques de prix et les volumes 
    pour anticiper les mouvements futurs. C'est un outil essentiel pour tout trader.
    """)

    # Sélection d'une action
    st.markdown("### 📈 Choisissez une action à analyser")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        action_selectionnee = st.selectbox(
            "Action:",
            options=list(ACTIONS_BRVM.keys())
        )

    with col2:
        periode = st.selectbox(
            "Période:",
            options=['30 jours', '90 jours', '180 jours', '1 an'],
            index=1
        )

    with col3:
        type_graphique = st.selectbox(
            "Type:",
            options=['Chandelier', 'Ligne', 'Aires']
        )

    # Conversion de la période en jours
    jours_map = {'30 jours': 30, '90 jours': 90, '180 jours': 180, '1 an': 365}
    jours = jours_map[periode]

    # Génération des données
    df_prix = generer_historique_prix(action_selectionnee, jours)
    df_prix = calculer_indicateurs_techniques(df_prix)

    # Informations sur l'action
    info_action = ACTIONS_BRVM[action_selectionnee]

    st.markdown("---")

    # Métriques actuelles
    col1, col2, col3, col4 = st.columns(4)

    prix_actuel = df_prix['Prix'].iloc[-1]
    prix_initial = df_prix['Prix'].iloc[0]
    variation = ((prix_actuel - prix_initial) / prix_initial) * 100

    with col1:
        st.metric(
            "Prix Actuel",
            f"{prix_actuel:,.0f} FCFA",
            f"{variation:+.2f}%"
        )

    with col2:
        st.metric(
            "Plus Haut",
            f"{df_prix['Prix'].max():,.0f} FCFA"
        )

    with col3:
        st.metric(
            "Plus Bas",
            f"{df_prix['Prix'].min():,.0f} FCFA"
        )

    with col4:
        st.metric(
            "Secteur",
            info_action['secteur']
        )

    st.markdown("---")

    # Graphique principal
    if type_graphique == 'Chandelier':
        afficher_graphique_chandelier(df_prix, f"Cours de {action_selectionnee}")

    elif type_graphique == 'Ligne':
        fig = go.Figure()

        # Ligne de prix
        fig.add_trace(go.Scatter(
            x=df_prix['Date'],
            y=df_prix['Prix'],
            mode='lines',
            name='Prix',
            line=dict(color='#667eea', width=2)
        ))

        # Moyennes mobiles
        if len(df_prix) >= 20:
            fig.add_trace(go.Scatter(
                x=df_prix['Date'],
                y=df_prix['SMA_20'],
                mode='lines',
                name='SMA 20',
                line=dict(color='orange', width=1, dash='dash')
            ))

        if len(df_prix) >= 50:
            fig.add_trace(go.Scatter(
                x=df_prix['Date'],
                y=df_prix['SMA_50'],
                mode='lines',
                name='SMA 50',
                line=dict(color='red', width=1, dash='dash')
            ))

        fig.update_layout(
            title=f"Évolution du cours de {action_selectionnee}",
            yaxis_title='Prix (FCFA)',
            xaxis_title='Date',
            template='plotly_white',
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    else:  # Aires
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_prix['Date'],
            y=df_prix['Prix'],
            fill='tozeroy',
            name='Prix',
            line=dict(color='#667eea')
        ))

        fig.update_layout(
            title=f"Évolution du cours de {action_selectionnee}",
            yaxis_title='Prix (FCFA)',
            xaxis_title='Date',
            template='plotly_white',
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    # Indicateurs techniques
    st.markdown("### 📊 Indicateurs Techniques")

    tab1, tab2, tab3 = st.tabs(["Moyennes Mobiles", "RSI", "Volume"])

    with tab1:
        st.markdown("""
        #### 📈 Moyennes Mobiles (Moving Averages)

        Les moyennes mobiles lissent les variations de prix pour identifier les tendances.

        - **SMA 20** (orange): Tendance court terme
        - **SMA 50** (rouge): Tendance moyen terme

        **Signal d'achat**: Quand SMA 20 croise SMA 50 vers le haut  
        **Signal de vente**: Quand SMA 20 croise SMA 50 vers le bas
        """)

        # Graphique des moyennes mobiles
        if len(df_prix) >= 50:
            fig = go.Figure()

            fig.add_trace(go.Scatter(x=df_prix['Date'], y=df_prix['Prix'],
                                     name='Prix', line=dict(color='#667eea')))
            fig.add_trace(go.Scatter(x=df_prix['Date'], y=df_prix['SMA_20'],
                                     name='SMA 20', line=dict(color='orange', dash='dash')))
            fig.add_trace(go.Scatter(x=df_prix['Date'], y=df_prix['SMA_50'],
                                     name='SMA 50', line=dict(color='red', dash='dash')))

            fig.update_layout(title="Prix et Moyennes Mobiles", template='plotly_white', height=400)
            st.plotly_chart(fig, use_container_width=True)

            # Analyse automatique
            dernier_sma20 = df_prix['SMA_20'].iloc[-1]
            dernier_sma50 = df_prix['SMA_50'].iloc[-1]

            if dernier_sma20 > dernier_sma50:
                st.success("✅ Tendance haussière: SMA 20 au-dessus de SMA 50")
            else:
                st.warning("⚠️ Tendance baissière: SMA 20 en-dessous de SMA 50")

    with tab2:
        st.markdown("""
        #### 📉 RSI (Relative Strength Index)

        Le RSI mesure la force d'une tendance sur une échelle de 0 à 100.

        - **RSI > 70**: Action **suracheté** → Risque de correction baissière
        - **RSI < 30**: Action **survendue** → Opportunité d'achat possible
        - **RSI 30-70**: Zone neutre
        """)

        # Graphique RSI
        if len(df_prix) >= 14:
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df_prix['Date'],
                y=df_prix['RSI'],
                name='RSI',
                line=dict(color='purple')
            ))

            # Lignes de référence
            fig.add_hline(y=70, line_dash="dash", line_color="red",
                          annotation_text="Suracheté (70)")
            fig.add_hline(y=30, line_dash="dash", line_color="green",
                          annotation_text="Survendu (30)")

            fig.update_layout(
                title="Indice de Force Relative (RSI)",
                yaxis_title="RSI",
                template='plotly_white',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

            # Analyse automatique
            dernier_rsi = df_prix['RSI'].iloc[-1]

            if dernier_rsi > 70:
                st.error(f"⚠️ RSI = {dernier_rsi:.1f} - Action suracheté, prudence !")
            elif dernier_rsi < 30:
                st.success(f"✅ RSI = {dernier_rsi:.1f} - Action survendu, opportunité possible !")
            else:
                st.info(f"ℹ️ RSI = {dernier_rsi:.1f} - Zone neutre")

    with tab3:
        st.markdown("""
        #### 📊 Volume de Transactions

        Le volume indique le nombre d'actions échangées. Un volume élevé confirme 
        la force d'un mouvement de prix.

        - **Volume croissant + hausse**: Tendance haussière forte
        - **Volume croissant + baisse**: Tendance baissière forte
        - **Volume faible**: Mouvement peu significatif
        """)

        # Graphique de volume
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_prix['Date'],
            y=df_prix['Volume'],
            name='Volume',
            marker_color='lightblue'
        ))

        fig.update_layout(
            title="Volume de Transactions",
            yaxis_title="Volume",
            template='plotly_white',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Statistiques de volume
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Volume Moyen", f"{df_prix['Volume'].mean():,.0f}")
        with col2:
            st.metric("Volume Max", f"{df_prix['Volume'].max():,.0f}")
        with col3:
            st.metric("Volume Actuel", f"{df_prix['Volume'].iloc[-1]:,.0f}")

    st.markdown("---")

    # Section éducative
    st.markdown("### 📚 En savoir plus sur l'analyse technique")

    with st.expander("🔍 Comment utiliser l'analyse technique ?"):
        st.markdown("""
        L'analyse technique est basée sur 3 principes:

        1. **Le marché intègre tout**: Les prix reflètent toutes les informations disponibles
        2. **Les prix évoluent en tendances**: Haussière, baissière ou latérale
        3. **L'histoire se répète**: Les patterns se reproduisent

        **Conseils pour débutants**:
        - Ne vous fiez jamais à un seul indicateur
        - Combinez analyse technique et analyse fondamentale
        - Pratiquez sur le simulateur avant d'investir réellement
        - Les indicateurs donnent des probabilités, pas des certitudes
        """)

    with st.expander("📖 Autres indicateurs populaires"):
        st.markdown("""
        - **MACD**: Convergence/Divergence de moyennes mobiles
        - **Bandes de Bollinger**: Mesure de la volatilité
        - **Stochastique**: Indicateur de momentum
        - **Volume Profile**: Distribution des volumes par niveau de prix
        - **Ichimoku**: Système complet d'analyse de tendance
        """)


def page_simulateur_trading():
    """
    Module de simulation de trading
    Permet aux étudiants de pratiquer sans risque
    """
    st.title("💰 Simulateur de Trading BRVM")

    st.markdown("""
    Pratiquez le trading avec **1 000 000 FCFA virtuels** sans aucun risque ! 
    Testez vos stratégies et apprenez de vos erreurs.
    """)

    # Affichage du portfolio
    st.markdown("### 💼 Votre Portfolio")

    col1, col2, col3, col4 = st.columns(4)

    # Calcul de la valeur totale du portfolio
    valeur_actions = sum(
        ACTIONS_BRVM[action]['prix'] * quantite
        for action, quantite in st.session_state.portfolio['stocks'].items()
    )
    valeur_totale = st.session_state.portfolio['cash'] + valeur_actions

    with col1:
        st.metric(
            "💵 Liquidités",
            f"{st.session_state.portfolio['cash']:,.0f} FCFA"
        )

    with col2:
        st.metric(
            "📊 Valeur Actions",
            f"{valeur_actions:,.0f} FCFA"
        )

    with col3:
        st.metric(
            "💎 Valeur Totale",
            f"{valeur_totale:,.0f} FCFA"
        )

    with col4:
        performance = ((valeur_totale - 1000000) / 1000000) * 100
        st.metric(
            "📈 Performance",
            f"{performance:+.2f}%"
        )

    st.markdown("---")

    # Tabs pour les différentes actions
    tab1, tab2, tab3, tab4 = st.tabs(["🛒 Acheter", "💸 Vendre", "📊 Mes Positions", "📜 Historique"])

    with tab1:
        st.markdown("### 🛒 Acheter des Actions")

        col1, col2 = st.columns([2, 1])

        with col1:
            # Sélection de l'action à acheter
            action_achat = st.selectbox(
                "Action à acheter:",
                options=list(ACTIONS_BRVM.keys()),
                key='action_achat'
            )

            prix_action = ACTIONS_BRVM[action_achat]['prix']
            secteur = ACTIONS_BRVM[action_achat]['secteur']

            st.info(f"""
            **{action_achat}**  
            Secteur: {secteur}  
            Prix actuel: **{prix_action:,} FCFA**
            """)

            # Quantité à acheter
            quantite_achat = st.number_input(
                "Quantité à acheter:",
                min_value=1,
                max_value=int(st.session_state.portfolio['cash'] / prix_action),
                value=1,
                key='quantite_achat'
            )

            cout_total = prix_action * quantite_achat
            frais = cout_total * 0.01  # 1% de frais de courtage
            cout_total_avec_frais = cout_total + frais

            st.markdown(f"""
            **Récapitulatif de l'achat:**
            - Prix unitaire: {prix_action:,} FCFA
            - Quantité: {quantite_achat}
            - Coût: {cout_total:,} FCFA
            - Frais (1%): {frais:,} FCFA
            - **Total: {cout_total_avec_frais:,} FCFA**
            """)

            # Bouton d'achat
            if st.button("✅ Confirmer l'achat", type="primary", key='btn_achat'):
                if cout_total_avec_frais <= st.session_state.portfolio['cash']:
                    # Mise à jour du portfolio
                    st.session_state.portfolio['cash'] -= cout_total_avec_frais

                    if action_achat in st.session_state.portfolio['stocks']:
                        st.session_state.portfolio['stocks'][action_achat] += quantite_achat
                    else:
                        st.session_state.portfolio['stocks'][action_achat] = quantite_achat

                    # Enregistrement dans l'historique
                    st.session_state.portfolio['history'].append({
                        'date': datetime.now(),
                        'action': action_achat,
                        'type': 'ACHAT',
                        'quantite': quantite_achat,
                        'prix': prix_action,
                        'total': cout_total_avec_frais
                    })

                    st.success(f"✅ Achat réussi ! Vous avez acheté {quantite_achat} actions {action_achat}")
                    st.rerun()
                else:
                    st.error("❌ Fonds insuffisants pour cet achat !")

        with col2:
            # Graphique de l'action sélectionnée
            df_prix = generer_historique_prix(action_achat, 30)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_prix['Date'],
                y=df_prix['Prix'],
                mode='lines',
                fill='tozeroy',
                name=action_achat,
                line=dict(color='#667eea')
            ))

            fig.update_layout(
                title=f"Évolution {action_achat} (30j)",
                template='plotly_white',
                height=300,
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 💸 Vendre des Actions")

        if len(st.session_state.portfolio['stocks']) == 0:
            st.warning("📭 Vous ne possédez aucune action à vendre.")
        else:
            col1, col2 = st.columns([2, 1])

            with col1:
                # Sélection de l'action à vendre
                action_vente = st.selectbox(
                    "Action à vendre:",
                    options=list(st.session_state.portfolio['stocks'].keys()),
                    key='action_vente'
                )

                quantite_possedee = st.session_state.portfolio['stocks'][action_vente]
                prix_action = ACTIONS_BRVM[action_vente]['prix']

                st.info(f"""
                **{action_vente}**  
                Quantité possédée: **{quantite_possedee}**  
                Prix actuel: **{prix_action:,} FCFA**
                """)

                # Quantité à vendre
                quantite_vente = st.number_input(
                    "Quantité à vendre:",
                    min_value=1,
                    max_value=quantite_possedee,
                    value=1,
                    key='quantite_vente'
                )

                gain_brut = prix_action * quantite_vente
                frais = gain_brut * 0.01  # 1% de frais
                gain_net = gain_brut - frais

                st.markdown(f"""
                **Récapitulatif de la vente:**
                - Prix unitaire: {prix_action:,} FCFA
                - Quantité: {quantite_vente}
                - Gain brut: {gain_brut:,} FCFA
                - Frais (1%): {frais:,} FCFA
                - **Gain net: {gain_net:,} FCFA**
                """)

                # Bouton de vente
                if st.button("✅ Confirmer la vente", type="primary", key='btn_vente'):
                    # Mise à jour du portfolio
                    st.session_state.portfolio['cash'] += gain_net
                    st.session_state.portfolio['stocks'][action_vente] -= quantite_vente

                    # Suppression si quantité = 0
                    if st.session_state.portfolio['stocks'][action_vente] == 0:
                        del st.session_state.portfolio['stocks'][action_vente]

                    # Enregistrement dans l'historique
                    st.session_state.portfolio['history'].append({
                        'date': datetime.now(),
                        'action': action_vente,
                        'type': 'VENTE',
                        'quantite': quantite_vente,
                        'prix': prix_action,
                        'total': gain_net
                    })

                    st.success(f"✅ Vente réussie ! Vous avez vendu {quantite_vente} actions {action_vente}")
                    st.rerun()

            with col2:
                # Graphique de l'action sélectionnée
                df_prix = generer_historique_prix(action_vente, 30)

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_prix['Date'],
                    y=df_prix['Prix'],
                    mode='lines',
                    fill='tozeroy',
                    name=action_vente,
                    line=dict(color='#dc3545')
                ))

                fig.update_layout(
                    title=f"Évolution {action_vente} (30j)",
                    template='plotly_white',
                    height=300,
                    showlegend=False
                )

                st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### 📊 Mes Positions Actuelles")

        if len(st.session_state.portfolio['stocks']) == 0:
            st.info("📭 Vous ne possédez actuellement aucune action.")
        else:
            # Création d'un DataFrame pour afficher les positions
            positions_data = []

            for action, quantite in st.session_state.portfolio['stocks'].items():
                prix_actuel = ACTIONS_BRVM[action]['prix']
                valeur = prix_actuel * quantite

                positions_data.append({
                    'Action': action,
                    'Secteur': ACTIONS_BRVM[action]['secteur'],
                    'Quantité': quantite,
                    'Prix Actuel': f"{prix_actuel:,} FCFA",
                    'Valeur Totale': f"{valeur:,} FCFA"
                })

            df_positions = pd.DataFrame(positions_data)
            st.dataframe(df_positions, use_container_width=True, hide_index=True)

            # Graphique de répartition du portfolio
            st.markdown("#### 📈 Répartition de votre portfolio")

            valeurs = [ACTIONS_BRVM[action]['prix'] * quantite
                       for action, quantite in st.session_state.portfolio['stocks'].items()]
            labels = list(st.session_state.portfolio['stocks'].keys())

            fig = px.pie(
                values=valeurs,
                names=labels,
                title='Répartition par action',
                color_discrete_sequence=px.colors.sequential.Purples
            )

            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("### 📜 Historique des Transactions")

        if len(st.session_state.portfolio['history']) == 0:
            st.info("📭 Aucune transaction effectuée pour le moment.")
        else:
            # Création d'un DataFrame pour l'historique
            historique_data = []

            for transaction in reversed(st.session_state.portfolio['history']):
                historique_data.append({
                    'Date': transaction['date'].strftime('%Y-%m-%d %H:%M:%S'),
                    'Type': transaction['type'],
                    'Action': transaction['action'],
                    'Quantité': transaction['quantite'],
                    'Prix': f"{transaction['prix']:,} FCFA",
                    'Total': f"{transaction['total']:,} FCFA"
                })

            df_historique = pd.DataFrame(historique_data)
            st.dataframe(df_historique, use_container_width=True, hide_index=True)

            # Statistiques
            st.markdown("#### 📊 Statistiques")

            nb_achats = len([t for t in st.session_state.portfolio['history'] if t['type'] == 'ACHAT'])
            nb_ventes = len([t for t in st.session_state.portfolio['history'] if t['type'] == 'VENTE'])

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Nombre d'achats", nb_achats)
            with col2:
                st.metric("Nombre de ventes", nb_ventes)
            with col3:
                st.metric("Total transactions", nb_achats + nb_ventes)

    st.markdown("---")

    # Bouton de réinitialisation
    st.markdown("### 🔄 Réinitialiser le Simulateur")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("🔄 Réinitialiser", type="secondary"):
            st.session_state.portfolio = {
                'cash': 1000000,
                'stocks': {},
                'history': []
            }
            st.success("✅ Portfolio réinitialisé avec 1 000 000 FCFA")
            st.rerun()

    with col2:
        st.info("Recommence avec 1M FCFA")


def page_quiz():
    """
    Module de quiz et évaluation
    Teste les connaissances des étudiants
    """
    st.title("🎯 Quiz & Évaluation")

    st.markdown("""
    Testez vos connaissances sur la BRVM et la bourse ! 
    Ce quiz comprend 10 questions de niveaux variés.
    """)

    # Questions du quiz
    QUESTIONS = [
        {
            'question': "Que signifie BRVM ?",
            'options': [
                "Banque Régionale des Valeurs Mobilières",
                "Bourse Régionale des Valeurs Mobilières",
                "Bureau Régional des Valeurs Monétaires",
                "Bourse des Valeurs du Mali"
            ],
            'reponse': 1,
            'explication': "BRVM signifie Bourse Régionale des Valeurs Mobilières."
        },
        {
            'question': "En quelle année a été créée la BRVM ?",
            'options': ["1995", "1998", "2000", "2005"],
            'reponse': 1,
            'explication': "La BRVM a été créée en 1998 dans le cadre de l'intégration de l'UEMOA."
        },
        {
            'question': "Combien de pays composent l'UEMOA et donc la BRVM ?",
            'options': ["6 pays", "7 pays", "8 pays", "10 pays"],
            'reponse': 2,
            'explication': "L'UEMOA regroupe 8 pays d'Afrique de l'Ouest."
        },
        {
            'question': "Qu'est-ce qu'une action ?",
            'options': [
                "Un prêt fait à une entreprise",
                "Une part du capital d'une entreprise",
                "Un compte d'épargne",
                "Une assurance"
            ],
            'reponse': 1,
            'explication': "Une action représente une fraction du capital d'une entreprise."
        },
        {
            'question': "Qu'est-ce qu'un dividende ?",
            'options': [
                "Le prix d'achat d'une action",
                "Les frais de courtage",
                "Une part des bénéfices distribuée aux actionnaires",
                "Un impôt sur les actions"
            ],
            'reponse': 2,
            'explication': "Le dividende est la partie du bénéfice redistribuée aux actionnaires."
        },
        {
            'question': "Quelle est la devise utilisée à la BRVM ?",
            'options': ["Euro", "Dollar", "Franc CFA", "Naira"],
            'reponse': 2,
            'explication': "Les transactions à la BRVM se font en Franc CFA (XOF)."
        },
        {
            'question': "Que signifie un RSI supérieur à 70 ?",
            'options': [
                "Action sous-évaluée",
                "Action suracheté",
                "Action en faillite",
                "Action recommandée"
            ],
            'reponse': 1,
            'explication': "Un RSI > 70 indique que l'action est suracheté et risque une correction."
        },
        {
            'question': "Qu'est-ce qu'une obligation ?",
            'options': [
                "Une part d'une entreprise",
                "Un titre de créance",
                "Un compte bancaire",
                "Un contrat d'assurance"
            ],
            'reponse': 1,
            'explication': "Une obligation est un titre de créance : vous prêtez de l'argent contre des intérêts."
        },
        {
            'question': "Quelle stratégie consiste à acheter et conserver longtemps ?",
            'options': [
                "Day Trading",
                "Scalping",
                "Buy and Hold",
                "Swing Trading"
            ],
            'reponse': 2,
            'explication': "Le 'Buy and Hold' consiste à acheter et garder ses actions sur le long terme."
        },
        {
            'question': "Où est situé le siège de la BRVM ?",
            'options': [
                "Dakar, Sénégal",
                "Abidjan, Côte d'Ivoire",
                "Bamako, Mali",
                "Ouagadougou, Burkina Faso"
            ],
            'reponse': 1,
            'explication': "Le siège de la BRVM est situé à Abidjan en Côte d'Ivoire."
        }
    ]

    # Initialisation du quiz si nécessaire
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}

    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

    # Affichage des questions
    if not st.session_state.quiz_submitted:
        st.markdown("### 📝 Répondez aux questions suivantes:")

        for idx, question in enumerate(QUESTIONS):
            st.markdown(f"""
            <div class="quiz-question">
                <strong>Question {idx + 1}/10:</strong> {question['question']}
            </div>
            """, unsafe_allow_html=True)

            reponse = st.radio(
                f"Votre réponse à la question {idx + 1}:",
                options=question['options'],
                key=f"q_{idx}",
                label_visibility="collapsed"
            )

            st.session_state.quiz_answers[idx] = reponse

            st.markdown("---")

        # Bouton de soumission
        col1, col2, col3 = st.columns([1, 1, 2])
        with col2:
            if st.button("✅ Soumettre le Quiz", type="primary"):
                st.session_state.quiz_submitted = True
                st.rerun()

    else:
        # Affichage des résultats
        st.markdown("### 📊 Résultats du Quiz")

        # Calcul du score
        score = 0
        for idx, question in enumerate(QUESTIONS):
            reponse_utilisateur = st.session_state.quiz_answers.get(idx)
            reponse_correcte = question['options'][question['reponse']]

            if reponse_utilisateur == reponse_correcte:
                score += 1

        pourcentage = (score / len(QUESTIONS)) * 100

        # Affichage du score global
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Score", f"{score}/{len(QUESTIONS)}")
        with col2:
            st.metric("Pourcentage", f"{pourcentage:.0f}%")
        with col3:
            if pourcentage >= 80:
                mention = "🏆 Excellent"
            elif pourcentage >= 60:
                mention = "✅ Bien"
            elif pourcentage >= 40:
                mention = "⚠️ Passable"
            else:
                mention = "❌ À revoir"
            st.metric("Mention", mention)

        # Message de félicitations ou encouragement
        if pourcentage >= 80:
            st.success("""
            🎉 **Félicitations !** Vous maîtrisez très bien les concepts de la BRVM. 
            Vous êtes prêt à passer au trading réel !
            """)
        elif pourcentage >= 60:
            st.info("""
            👍 **Bon travail !** Vous avez de bonnes bases. 
            Revoyez les concepts où vous avez des faiblesses.
            """)
        else:
            st.warning("""
            📚 **Continuez à apprendre !** Prenez le temps de revoir les modules de formation 
            avant de commencer à trader.
            """)

        st.markdown("---")

        # Détail des réponses
        st.markdown("### 📋 Détail des Réponses")

        for idx, question in enumerate(QUESTIONS):
            reponse_utilisateur = st.session_state.quiz_answers.get(idx)
            reponse_correcte = question['options'][question['reponse']]

            est_correct = reponse_utilisateur == reponse_correcte

            with st.expander(
                    f"{'✅' if est_correct else '❌'} Question {idx + 1}: {question['question']}"
            ):
                st.markdown(f"**Votre réponse:** {reponse_utilisateur}")
                st.markdown(f"**Réponse correcte:** {reponse_correcte}")

                if est_correct:
                    st.success(f"✅ Correct ! {question['explication']}")
                else:
                    st.error(f"❌ Incorrect. {question['explication']}")

        st.markdown("---")

        # Boutons d'action
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Recommencer le Quiz"):
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()

        with col2:
            if st.button("📚 Retour aux Modules"):
                st.session_state.current_module = "Accueil"
                st.rerun()


# ==========================================
# NAVIGATION ET EXÉCUTION
# ==========================================

def changer_module(module):
    """Change le module affiché lorsque l'utilisateur clique sur un bouton."""
    st.session_state.current_module = module


def main():
    """
    Fonction principale qui gère la navigation et l'affichage
    """
    # Sidebar pour la navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=BRVM+Formation",
                 use_column_width=True)

        st.markdown("## 📚 Modules de Formation")

        # Menu de navigation
        menu_items = {
            "🏠 Accueil": "Accueil",
            "🏛️ Introduction BRVM": "Introduction",
            "📚 Concepts Fondamentaux": "Concepts",
            "📊 Analyse Technique": "Analyse",
            "💰 Simulateur Trading": "Simulateur",
            "🎯 Quiz & Évaluation": "Quiz"
        }

        # Chaque bouton met à jour le module via un callback Streamlit.
        # Le rerun est alors déclenché automatiquement après le clic.
        for label, key in menu_items.items():
            libelle_bouton = f"▶ {label}" if st.session_state.current_module == key else label
            st.button(
                libelle_bouton,
                key=f"nav_{key}",
                use_container_width=True,
                on_click=changer_module,
                args=(key,)
            )

        st.markdown("---")

        # Informations dans la sidebar
        st.markdown("### 💡 Conseils")
        st.info("""
        - Suivez les modules dans l'ordre
        - Pratiquez avec le simulateur
        - Testez vos connaissances avec le quiz
        """)

        st.markdown("---")

        # Statistiques de progression
        st.markdown("### 📊 Votre Progression")

        progression = 0
        if st.session_state.portfolio['history']:
            progression += 30
        if st.session_state.quiz_submitted:
            progression += 40
        if len(st.session_state.portfolio['stocks']) > 0:
            progression += 30

        st.progress(min(progression / 100, 1.0))
        st.markdown(f"**{min(progression, 100)}%** complété")

    # Affichage du module sélectionné
    if st.session_state.current_module == "Accueil":
        page_accueil()
    elif st.session_state.current_module == "Introduction":
        page_introduction()
    elif st.session_state.current_module == "Concepts":
        page_concepts_fondamentaux()
    elif st.session_state.current_module == "Analyse":
        page_analyse_technique()
    elif st.session_state.current_module == "Simulateur":
        page_simulateur_trading()
    elif st.session_state.current_module == "Quiz":
        page_quiz()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>📚 Application Éducative BRVM - Formation à la Bourse</p>
        <p>Développée par le Servie Communication et Marketing de la BRVM | © 2026</p>
        <p style='font-size: 0.9em;'>⚠️ Les données de cette application sont à but éducatif uniquement</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# POINT D'ENTRÉE
# ==========================================
if __name__ == "__main__":
    main()