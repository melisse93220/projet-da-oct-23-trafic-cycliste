# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 20:11:07 2023

@author: Melissa
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


df = pd.read_csv('trafic.csv')

st.sidebar.title('Le trafic cycliste à Paris')

pages = ["Introduction du projet", "Exploration des données", "Analyse des données avec DataViz", "Nettoyage et pré-processing", "Modélisation", "Conclusion et perspective"]

page = st.sidebar.radio("Aller vers", pages)
st.sidebar.markdown("---")

st.sidebar.write(":blue[**Ce projet a été réalisé et présenté par :**]")
st.sidebar.write(":blue[Mélissa Bouchaïb]")
st.sidebar.write(":blue[Ouarda Costa Dos Santos]")
st.sidebar.write(":blue[Solofo Rambeloarison]")
st.sidebar.markdown("---")
st.sidebar.write("**Formation Data Analyst**")
st.sidebar.write("**Bootcamp Octobre 2023**")

if page == pages[0] : 
    st.write("## **Introduction du projet**")
    
    st.image("image1.jpg")
    
    st.markdown("#### :violet[Contexte]")
    
    st.write("Du point de vue technique, la Ville de Paris a déployé des compteurs à vélo permanents depuis plusieurs années pour évaluer le développement de la pratique cycliste. Cette initiative s'inscrit dans une tendance globale de promotion de la mobilité douce et durable au sein de la ville.")
    st.write("Sur le plan économique, il est essentiel d'optimiser les investissements dans les infrastructures cyclables en s'appuyant sur des données fiables. Cela permettra d'améliorer l'efficacité des ressources allouées à l'entretien et au développement des voies cyclables.")
    st.write("Sur le plan scientifique, cette analyse des données des compteurs vélo nous offre l'opportunité de comprendre les modèles de comportement des cyclistes en ville. Cela contribue à une meilleure gestion du réseau cyclable et à une réduction de l'empreinte carbone.")
    
    st.markdown("#### :violet[Objectifs]")
    
    st.write(
    """
    Les principaux objectifs de ce projet sont les suivants :
    - Analyser les données collectées par les compteurs vélo pour identifier les horaires et les zones d'affluence des cyclistes.
    - Fournir des outils de visualisation à la Mairie de Paris pour évaluer et améliorer les infrastructures cyclables en fonction des besoins de la communauté cycliste.
    """
    )
        
    st.markdown("#### :violet[Compréhension et Manipulation des données]")
    st.write("**Cadre**")
    st.write("Pour ce projet, nous avons utilisé les données recueillies par les compteurs à vélo permanents au nombre total de 71 déployés dans la ville de Paris situés à côté des zones cyclables. Ces données sont disponibles en interne et sont la propriété de la Mairie. La volumétrie de ces données est considérable, couvrant de nombreuses périodes et des zones variées de la ville.")
    st.write("**Pertinence**")
    st.write("Les variables les plus pertinentes pour notre analyse sont, par exemple, le nombre de passages de vélos par heure, la localisation des compteurs, et d'autres données contextuelles qui nous aideront à comprendre les comportements des cyclistes. La variable cible principale est le nombre de passages de vélos par heure, car c'est elle qui reflète l'affluence cycliste.")
    st.write("Certaines particularités de ces données incluent des périodes de pointe pendant les heures de travail et des variations saisonnières.")
    st.write("**Visualisations et Statistiques**")
    st.write("Dans la phase de visualisation, nous avons identifié des corrélations entre les variables telles que l'heure de la journée et le nombre de passages de vélos. Nous avons également analysé la distribution des données, identifiant des pics d'activité, des variations saisonnières. Ces observations ont été confirmées par des analyses statistiques appropriées.")
    st.write("En conclusion, cette phase exploratoire des données nous a permis de mieux comprendre le comportement des cyclistes à Paris, et nous avons identifié des tendances et des informations clés qui guideront notre modélisation future pour optimiser les infrastructures cyclables de la ville.")
    
elif page == pages[1] :
    st.write("## **Exploration des données**")
    
    st.markdown("#### :violet[Aperçu du Dataframe]")
    st.dataframe(df.head())
    
    st.write("Afin de fournir à la Mairie de Paris des outils d'analyse afin d'évaluer et d'améliorer les infrastructures cyclables de la ville, une analyse croisée relative au réseau cyclable peut être utilisée en utilisant les données de comptage de vélos.")
    st.write("L’analyse du réseau des pistes cyclables joue un rôle primordial dans l’optimisation de l’infrastructure existante et dans l’identification des besoins en termes de nouvelles connexions ou améliorations. Elle contribue également à une meilleure planification urbaine, en assurant une accessibilité et une couverture complètes par le réseau cyclable, et en améliorant l’expérience globale des cyclistes.")
    st.write("En fusionnant ces deux datasets, la ville peut non seulement encourager davantage de personnes à opter pour le vélo comme moyen de transport mais aussi à favoriser un cadre de vie urbain plus durable et agréable.")
    
    st.markdown("#### :violet[Analyse exploratoire]")
    st.write("**Voici ci-dessous une analyse exploratoire du Dataset principal – Comptage vélos / données compteurs et du Dataset secondaire – Réseau des itinéraires cyclables utilisés pour ce projet.**")
    st.image("image2.jpg")
    
elif page == pages[2]:
    visualisations = st.selectbox(
        label=":violet[Choisissez une visualisation]", 
        options=[
            'VISUALISATION 1 – TRAFIC CYCLISTE MOYEN PAR HEURE DE LA JOURNÉE', 
            'VISUALISATION 2 – TRAFIC CYCLISTE MOYEN PAR JOUR DE LA SEMAINE', 
            'VISUALISATION 3 – TRAFIC CYCLISTE PAR MOIS AVEC MÉDIANE ET MOYENNE ANNUELLE', 
            'VISUALISATION 4 – TOP 10 DES SITES AVEC LE PLUS ET LE MOINS DE COMPTAGE', 
            'VISUALISATION 5 – REPRÉSENTATION CARTOGRAPHIQUE DES COMPTEURS VELOS'
        ]
    )

    if visualisations == 'VISUALISATION 1 – TRAFIC CYCLISTE MOYEN PAR HEURE DE LA JOURNÉE':
        hourly_traffic = df.groupby('heure')['Comptage horaire'].mean().reset_index()
        # Visualisation avec Plotly
        fig_h = px.bar(hourly_traffic, x='heure', y='Comptage horaire',
                     labels={'Comptage horaire': 'Comptage Horaire Moyen'},
                     title='Trafic Cycliste Moyen en Fonction de l\'Heure de la Journée')

        # Personnalisation supplémentaire (si nécessaire)
        fig_h.update_layout(xaxis_title='Heure de la Journée',
                          yaxis_title='Comptage Horaire Moyen',
                          title_x=0.3,
                          plot_bgcolor='rgba(0,0,0,0)',# Fond transparent
                          width=800,
                          height=600)
        fig_h.update_xaxes(tickvals=list(hourly_traffic['heure']))
        # Affichage de la figure
        st.plotly_chart(fig_h)
        
        #st.image("visualisation1.jpg")
        
        st.write(":orange[**Commentaire d'analyse**]")
        st.write("Le pic de trafic cycliste semble se produire aux alentours de 8 et 9 heures et de 17 à 18 heures. Cela pourrait correspondre aux heures de pointe du matin et du soir, indiquant que de nombreuses personnes utilisent leur vélo pour se rendre au travail ou en revenir.")
        st.write("Il y a une baisse significative du trafic entre 9 heures et 16 heures, avec une augmentation légère durant l'heure du déjeuner (environ 12 heures).")
        st.write("Le trafic est relativement faible très tôt le matin (de 0 à 6 heures) et tard le soir (après 21 heures).")
        st.write("Les périodes les moins fréquentées sont entre 1 et 5 heures du matin, ce qui est prévisible puisque la plupart des gens dorment à ces heures.")
        st.write("En résumé, le graphique suggère que le vélo est principalement utilisé pour les trajets domicile-travail, avec des pics d'activité correspondant aux heures de début et de fin de journée de travail typiques. Il y a moins d'activité cycliste pendant les heures creuses et très peu pendant la nuit.")
        
        st.write(":orange[**Validation statistique**]")
        st.write("Les statistiques calculées confirment les observations visuelles : Les heures de pointe matinales (8h-9h) et du soir (18h-19h) présentent les moyennes et médianes les plus élevées, indiquant un trafic cycliste plus important durant ces périodes.")
        st.write("Le trafic cycliste est relativement faible durant la nuit et les premières heures du matin (1h-6h), avec des moyennes et médianes basses. ")
        st.write("Il y a également une augmentation notable du trafic en milieu de journée, particulièrement autour de 12h-14h.")
        st.write("En conclusion, ces tendances sont cohérentes avec les comportements typiques de déplacement domicile-travail et pourraient être influencées par les horaires de travail et scolaires.")

    elif visualisations == 'VISUALISATION 2 – TRAFIC CYCLISTE MOYEN PAR JOUR DE LA SEMAINE':
        # jours_de_la_semaine doit être défini avant de l'utiliser pour mapper les valeurs.
        jours_de_la_semaine = {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi', 5: 'Samedi', 6: 'Dimanche'}
        df['nom_jour'] = df['Jour de la semaine'].map(jours_de_la_semaine)

        # Calcul du trafic cycliste moyen par jour de la semaine

        moyenne_par_jour = df.groupby('nom_jour')['Comptage horaire'].mean().reindex(jours_de_la_semaine.values())

        # Création du diagramme en barres avec Plotly
        fig_j = px.bar(moyenne_par_jour, x=moyenne_par_jour.index, y=moyenne_par_jour.values, labels={'y':'Comptage Horaire Moyen', 'index':'Jour de la Semaine'}, title='Trafic Cycliste Moyen par Jour de la Semaine')
        fig_j.update_layout(xaxis_title='Jour de la Semaine',title_x=0.3,yaxis_title='Comptage Horaire Moyen', xaxis_tickangle=-45,  width=800, height=600)
        #fig_j.update_xaxes(tickvals=list(hourly_traffic['heure']))
        st.plotly_chart(fig_j)
        
        #st.image("visualisation2.jpg")
        
        st.write(":orange[**Commentaire d'analyse**]")
        st.write("Le trafic cycliste est plus élevé en milieu de semaine du mardi au jeudi avec un pic le mercredi, ce qui pourrait indiquer une tendance plus forte à utiliser le vélo pour les déplacements en semaine.")
        st.write("Le lundi et le vendredi présente le nombre le plus faible de cyclistes en semaine, ce qui pourrait suggérer une moindre activité au début de la semaine. Cela peut peut-être s'expliquer par la mise en place du télétravail 1 ou 2 par semaine selon les entreprises.")
        st.write("Il y a une diminution notable du trafic le vendredi, suivie d'une baisse plus prononcée pendant le week-end. Cela suggère que le vélo est moins utilisé pour les loisirs ou les courses pendant le week-end, ou que les gens préfèrent d'autres modes de transport pendant ces jours.")
        st.write("Le dimanche a le trafic le plus faible, ce qui pourrait indiquer que c'est le jour de repos principal pour la majorité des cyclistes dans cette région.")
        st.write("En résumé, le graphique suggère que le vélo est principalement utilisé pour les déplacements réguliers en semaine (domicile-travail ou domicile-école), avec une activité cycliste qui diminue progressivement vers la fin de la semaine et atteint son point le plus bas le dimanche.")
        
        st.write(":orange[**Validation statistique**]")
        st.write("Le calcul de la p-value faible permet de rejeter l'hypothèse nulle, confirmant qu'il existe une différence significative entre le trafic cycliste moyen durant les jours ouvrables et les weekends.")
        st.write("Ceci valide notre observation initiale basée sur la visualisation.")

    elif visualisations == 'VISUALISATION 3 – TRAFIC CYCLISTE PAR MOIS AVEC MÉDIANE ET MOYENNE ANNUELLE':
        median_annuelle = df['Comptage horaire'].median()
        moyenne_annuelle = df['Comptage horaire'].mean()
        grp_mois = df.groupby('annee_mois')['Comptage horaire'].mean().reset_index()

        # Créez un graphique à barres pour afficher la moyenne par mois avec Plotly
        fig_m = go.Figure()

        # Ajoutez les barres pour la moyenne mensuelle
        fig_m.add_trace(go.Bar(
            x=grp_mois['annee_mois'],
            y=grp_mois['Comptage horaire'],
            name='Moyenne Mensuelle',
            marker_color='lightcoral'
        ))

        # Ajoutez une ligne horizontale pour la médiane annuelle
        fig_m.add_hline(y=median_annuelle, line_dash="dash", line_color="blue", annotation_text=f"Médiane Annuelle: {median_annuelle:.1f}", annotation_position="bottom right")

        # Ajoutez une ligne horizontale pour la moyenne annuelle
        fig_m.add_hline(y=moyenne_annuelle, line_dash="dot", line_color="green", annotation_text=f"Moyenne Annuelle: {moyenne_annuelle:.1f}", annotation_position="bottom right")

        # Titre et labels
        fig_m.update_layout(
            title='Trafic Cycliste Moyen par Mois avec Médiane et Moyenne Annuelles',
            title_x=0.3,
            xaxis_title='Année_Mois',
            yaxis_title='Comptage Horaire Moyen',
            xaxis_tickangle=-45,
            width=800,
            height=600,
            legend_title_text='Indicateurs'
        )
        fig_m.update_xaxes(tickvals=list(grp_mois['annee_mois']))
        st.plotly_chart(fig_m)
        
        #st.image("visualisation3.jpg")
        
        st.write(":orange[**Commentaire d'analyse**]")
        st.write("Il semble y avoir une saisonnalité dans le trafic cycliste, avec des pics durant certains mois (comme octobre, mars et mai) et des baisses notables durant d'autres (comme décembre et août).")
        st.write("Les mois d'hiver (décembre, janvier, février) montrent un déclin dans le trafic cycliste, ce qui est cohérent avec les conditions météorologiques plus difficiles pour le cyclisme.")
        st.write("Le mois d'août a le trafic le plus faible, ce qui pourrait correspondre aux vacances d'été où les gens sont moins susceptibles de se rendre au travail ou à l'école en vélo.")
        st.write("En résumé, le graphique suggère que le trafic cycliste varie considérablement tout au long de l'année, probablement en réponse à des facteurs saisonniers, des vacances, ainsi que d'autres modèles de déplacement annuels. La médiane étant inférieure à la moyenne, cela indique également que la distribution du trafic cycliste est asymétrique et qu'il y a des mois avec des valeurs très élevées qui augmentent la moyenne au-dessus de la médiane.")
        
        st.write(":orange[**Validation statistique**]")
        st.write("La p-value est inférieure au seuil de 0.05, ce qui permet de rejeter l'hypothèse nulle et de conclure qu'il existe une différence significative entre le trafic cycliste moyen durant les mois chauds et froids.")
        st.write("Cette différence statistiquement significative confirme notre observation visuelle d'une tendance saisonnière dans les données.")

    elif visualisations == 'VISUALISATION 4 – TOP 10 DES SITES AVEC LE PLUS ET LE MOINS DE COMPTAGE':
        # Groupement des données par site de comptage et calcul de la somme du comptage horaire pour chaque site
        site_traffic = df.groupby('Nom du site de comptage')['Comptage horaire'].sum().reset_index()
        # Triage des valeurs pour obtenir le top 10 des sites avec le plus de comptage et le moins de comptage
        top_10_sites = site_traffic.sort_values(by='Comptage horaire', ascending=False).head(10) 
        bottom_10_sites = site_traffic.sort_values(by='Comptage horaire', ascending=True).head(10)
        # Création de la visualisation pour le top 10 des sites avec le plus de comptage
        fig_top = px.bar(top_10_sites, x='Comptage horaire', y='Nom du site de comptage',
                 title='Top 10 des Sites avec le Plus de Comptage',
                 labels={'Comptage horaire': 'Comptage horaire total', 'Nom du site de comptage': 'Nom du site de comptage'},
                 orientation='h', color='Comptage horaire',
                 color_continuous_scale=px.colors.sequential.Blues)  # Blues_r pour une échelle de bleus inversée
        fig_top.update_layout(yaxis={'categoryorder':'total ascending'})  # Pour trier les barres par ordre décroissant
        # Création de la visualisation pour le top 10 des sites avec le moins de comptage
        fig_bottom = px.bar(bottom_10_sites, x='Comptage horaire', y='Nom du site de comptage',
                    title='Top 10 des Sites avec le Moins de Comptage',
                    labels={'Comptage horaire': 'Comptage horaire total', 'Nom du site de comptage': 'Nom du site de comptage'},
                    orientation='h', color='Comptage horaire',
                    color_continuous_scale=px.colors.sequential.Blues_r)  # Blues pour une échelle de bleus
        fig_bottom.update_layout(yaxis={'categoryorder':'total descending'})  # Pour trier les barres par ordre croissant
        # Pour le graphique du top 10 des sites avec le plus de comptage
        fig_top.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',  # Définit la couleur de fond du papier (zone extérieure) comme transparente
            plot_bgcolor='rgba(0,0,0,0)',    # Définit la couleur de fond du tracé (zone intérieure) comme transparente
            width=900,
            height=400
            )
        # Pour le graphique du top 10 des sites avec le moins de comptage
        fig_bottom.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',  # Définit la couleur de fond du papier (zone extérieure) comme transparente
            plot_bgcolor='rgba(0,0,0,0)',    # Définit la couleur de fond du tracé (zone intérieure) comme transparente
            width=900,
            height=400
            )
        # Affichage des figures
        st.plotly_chart(fig_top)
        st.plotly_chart(fig_bottom)
          
        #st.image("visualisation4.jpg")
        
        st.write(":orange[**Commentaire d'analyse**]")
        st.write("Le site avec le plus grand nombre de passages est **le Totem 73 boulevard de Sébastopol**, avec plus de 4 millions de passages.")
        st.write("Les sites sont classés par ordre décroissant de trafic, avec **le Totem 85 quai d'Austerlitz** ayant le moins de passages parmi les 10 premiers, mais tout de même un nombre significatif à environ 2 millions de passages.")
        st.write("Ce graphique est utile pour identifier les endroits les plus fréquentés par les cyclistes et les moins fréquentés, ce qui peut informer les décisions en matière d'infrastructure cyclable voire de maintenance. Il montre clairement les points chauds et les points froids du trafic cycliste dans la région parisienne.")

    elif visualisations == 'VISUALISATION 5 – REPRÉSENTATION CARTOGRAPHIQUE DES COMPTEURS VELOS':
        st.image("visualisation5.jpg")
        
        st.write(":orange[**Commentaire d'analyse**]")
        st.write("Les marqueurs rouges indiquent les 10 emplacements où le trafic cycliste est le plus élevé. Ces points sont principalement concentrés autour du centre de Paris, avec une forte présence le long de la Seine et dans les zones très fréquentées comme République, Louvre, Bourse et Bastille. Cela suggère que ces zones sont des axes majeurs pour le cyclisme, peut-être en raison de la proximité des centres d'affaires, des lieux de loisirs ou de la présence de pistes cyclables.")
        st.write("Les marqueurs verts indiquent les 10 emplacements les moins fréquentés pour le cyclisme. Ils sont dispersés dans différentes parties de la ville, indiquant des zones qui pourraient être résidentielles, moins bien desservies par les infrastructures cyclables, ou simplement moins fréquentées en général.")
        st.write("Les marqueurs bleus représentent les autres compteurs de trafic cycliste qui ne font pas partie des 10 plus ou moins fréquentés. Leur répartition sur la carte montre que le suivi du trafic cycliste est une pratique répandue dans la ville, couvrant un large éventail de quartiers et fournissant une vue d'ensemble de la mobilité cycliste à Paris. On s'aperçoit que la Rive gauche de Paris possède plus de compteurs que la Rive droite où certains arrondissements parisiens n'ont aucuns compteurs : c'est le cas notamment pour le 8ième, 9ième, 16ième, 17ième, 18ième voire 20ième arrondissements de Paris.")
        st.write("Cette carte est un outil utile pour l'analyse de la mobilité urbaine et pourrait aider à l'optimisation des infrastructures cyclables, à l'identification des points noirs en termes de congestion et à la planification d'améliorations pour encourager le cyclisme dans les zones moins fréquentées.")
        
elif page == pages[3] :
    st.write("## **Nettoyage et pré-processing**")    
    
    st.markdown("#### :violet[Traitement des valeurs aberrantes]")
    
    if st.checkbox(":red[**Afficher les valeurs aberrantes avant suppression**] "):
       st.image("boxplot1.jpg")
    
    st.write(
    """
    Nous avons pu expliquer certaines valeurs extrêmes observées entre Juin et Août 2023, mais nous avons également détecté des valeurs aberrantes qui nécessitaient une analyse plus approfondie.
    - Au mois de juin, les valeurs extrêmes peuvent s'expliquer par l'évènement 'La Convergence' qui s'est déroulé à Paris le 11/06/2023.
    - Au mois de juillet, il y avait la dernière étape du Tour de France qui s'est déroulée à Paris le 20/07/2023.
    - Par contre, des valeurs aberrantes ont été enregistrées par les sites de comptage **'101003098' situé au 106 avenue Denfert Rochereau**, et **'100057380' positionné au niveau du Cours de la reine**. En effet, des valeurs anormalement élevées ont été observées entre juin 2023 et août 2023. Nous avons choisi de supprimer les valeurs aberrantes sur ces deux compteurs afin de ne pas fausser nos modélisations de prédiction de trafic étant donné que ces valeurs ne sont pas habituelles
    """
    )
    
    st.write("Les valeurs extrêmes sont capturées exclusivement par 2 sites de comptage à savoir le **'100003098'** et le **'100057380'**. Ces relevés exceptionnels ont été enregistrées entre juin 2023 et août 2023.")
    st.write("Afin de les repérer, nous avons calculé l'écart interquartile (IQR) des valeurs enregistrées par heure et par jour, et nous avons constaté des écarts significatifs entre celui-ci et les valeurs aberrantes. Nous avons choisi le **seuil de 500** pour isoler ces valeurs pour le site **'100003098'** et **3000 pour le site '100057380'**.")
    
    if st.checkbox(":red[**Afficher les valeurs aberrantes après suppression**] "):
       st.image("boxplot2.jpg")
    
    st.markdown("#### :violet[Analyse croisée avec le Dataset secondaire - Réseau cyclable]")
    st.write("Après le nettoyage et la fusion du Dataset principal et du Dataset secondaire, une correspondance de 56 sites de comptage du Dataset secondaire a été trouvé sur les 71 du Dataset principal nous permettant ainsi d'identifier les zones bien desservies et les zones nécessitant des améliorations.")
    st.image("top10.jpg")
    st.image("flop10.jpg")
    
    st.write("La corrélation entre la densité des infrastructures cyclables et le trafic cycliste peut être influencée par de nombreux facteurs. Voici quelques explications possibles de ces phénomènes et des recommandations pour les aborder :")
    st.write("###### **Infrastructures cyclables à densité élevée mais à trafic faible**")
    st.write(":orange[**Qualité et connectivité**] : Même si une ville a un grand nombre de pistes cyclables, si celles-ci ne sont pas bien connectées entre elles ou ne mènent pas aux destinations souhaitées (comme le travail, l'école, les centres commerciaux), les cyclistes ne les utiliseront pas.")
    st.write(":orange[**Sécurité et entretien**] : Les pistes peuvent être sous-utilisées si elles ne sont pas bien entretenues, si les cyclistes ne s'y sentent pas en sécurité, ou si le design des infrastructures ne répond pas aux normes de sécurité.")
    st.write(":orange[**Conscience et accessibilité**] : Si les gens ne sont pas conscients des infrastructures disponibles ou si elles ne sont pas facilement accessibles en raison de barrières physiques ou de problèmes de design, le trafic cycliste sera faible.")
    
    st.write(
    """
    Recommandations :
    - Améliorer la connectivité des pistes cyclables avec les principaux points d'intérêt.
    - Assurer la sécurité et l'entretien régulier des pistes.
    - Mener des campagnes d'information pour sensibiliser à l'existence et aux avantages des infrastructures cyclables.
    - Assurer l'accessibilité universelle, y compris pour les personnes à mobilité réduite.
    """
    )
        
    st.write("###### **Infrastructures cyclables à densité faible mais à trafic élevé**")
    st.write(":orange[**Demande concentrée**] : Des pistes cyclables peuvent être surchargées si elles sont situées sur des itinéraires populaires ou des artères qui connectent directement avec de nombreux points d'intérêt.")
    st.write(":orange[**Absence d'alternatives**] :  Si peu de pistes cyclables sont disponibles, mais que le vélo reste le mode de transport le plus pratique ou économique, elles seront probablement surutilisées.")
    st.write(":orange[**Culture du vélo**] : Une forte culture cycliste dans une région peut mener à une utilisation élevée même avec des infrastructures limitées.")
    
    st.write(
    """
    Recommandations :
    - Investir dans l'expansion des pistes cyclables dans les zones à forte demande.
    - Créer des réseaux cyclables qui offrent des alternatives aux itinéraires surchargés.
    - Encourager les partenariats avec des organisations locales pour promouvoir une culture du vélo durable.
    """
    )
    
elif page == pages[4] :
    st.write("## **Modélisation**")    
    
    st.markdown("#### :violet[Analyse des modèles initiaux]")
    st.write("Plusieurs modèles de régression ont été utilisés, incluant LinearRegression, Ridge, Lasso, DecisionTreeRegressor, RandomForestRegressor, et BaggingRegressor.")
    st.write("Voici les performances des modèles testés :")
    st.image("modeles.jpg")
    
    st.write(
    """
    - :orange[**LinearRegression, Ridge, Lasso**] : Tous ces modèles ont des valeurs de MSE très proches (8,728.53 pour LinearRegression et Ridge, légèrement moins élevé pour Lasso). Le MSE mesure la moyenne des carrés des erreurs, c'est-à-dire, la différence moyenne au carré entre les valeurs observées et les valeurs prédites. Plus le MSE est bas, mieux c'est. Cependant, ces valeurs semblent assez élevées. Les valeurs de R2, quant à elles, sont négatives ou très proches de zéro, ce qui indique que ces modèles ne sont pas du tout efficaces pour prédire la variable cible. Un R2 proche de 1 indiquerait une prédiction précise.
    - :orange[**DecisionTreeRegressor, RandomForestRegressor, BaggingRegressor**] : Ces trois modèles sont des méthodes d'apprentissage ensembliste. Le RandomForest et le Bagging sont des variations de l'arbre de décision, utilisant de multiples arbres pour améliorer la stabilité et la précision. Ces modèles basés sur des arbres de décision affichent également des performances médiocres, avec des MSE encore plus élevés et des R² négatifs. Cela pourrait indiquer un surajustement, surtout si les arbres sont très profonds, ou une mauvaise adaptation à la nature des données.
    """
    )
    
    st.write("Graphiquement parlant, l'une des limitations des modèles linéaires est leur nature continue et uniforme. Ils ne sont pas capables de capturer des relations complexes ou non linéaires entre les variables. Si les données présentent des tendances, des sauts, ou des comportements non linéaires, les modèles linéaires auront du mal à les modéliser correctement, ce qui se traduit par des prédictions pauvres et une ligne de prédiction relativement plate ou uniforme sur un graphique. De ce fait, seules les représentations graphiques issues des méthodes d’apprentissage ensembliste seront représentées afin de modéliser les prédictions de Juillet et Août 2023.")
    
    st.markdown("**Représentation graphique des modèles de prédiction de Juillet et Août 2023**")
    
    selected_model = st.selectbox('Choisissez un modèle', ['DecisionTreeRegressor', 'RandomForestRegressor', 'BaggingRegressor']) 
    selected_month = st.selectbox('Choisissez un mois', ['Juillet 2023', 'Août 2023']) 
    
    
    def get_image_path(model, month):  
        return f"images/{model.lower()}_{month.lower().replace(' ', '_')}.jpg" 

    image_path = get_image_path(selected_model, selected_month)   
    st.image(image_path, caption=f'{selected_model} - {selected_month}')
    
    st.write("Après avoir examiné les premières modélisations, il est devenu évident que, malgré certaines performances encourageantes, ces modèles présentent des limites significatives, notamment en ce qui concerne la précision des prévisions. Cette situation souligne la complexité des données de trafic cycliste, qui ne se prêtent pas simplement à des modèles linéaires ou même non linéaires classiques.")
    st.write("C'est dans ce contexte que l'introduction du modèle SARIMA représente une évolution logique de notre démarche analytique. En prenant en compte les aspects de saisonnalité et de non-stationnarité, qui sont des caractéristiques intrinsèques des données de trafic cycliste, le modèle SARIMA offre une perspective plus adaptée pour capturer et comprendre les tendances et les variations temporelles.") 
    st.write("Ainsi, en passant à l'approfondissement avec le modèle SARIMA, nous nous attendons à une meilleure adaptation du modèle aux données et, par conséquent, à des prévisions plus fiables et informatives pour la planification urbaine à Paris.")
    st.divider()
    st.markdown("#### :violet[Approfondissement avec le modèle SARIMA]") 
    @st.cache_data
    def load_data_st():
        df_trafic_st = pd.read_csv("df_trafic_st.csv", sep=',', index_col=0) 
        return df_trafic_st
    # mettre en index la date
    df_trafic_st = load_data_st() 
    
    if(st.checkbox('Afficher la série temporelle')): 
        st.markdown("###### :red[**01/09/2022 - 31/08/2023**]") 
        st.dataframe(df_trafic_st)

        demarche = st.radio("###### Méthode empirique :",['Analyse graphique', 'Analyse de stationnarité et test statistique', 'Stationnarisation de la série','Calcul et estimation des modéles', 'Choix du modèle et présentation graphique'])
        st.divider()

        if (demarche == 'Analyse graphique'):
            # Ajouter une colonne 'Date' basée sur l'index pour afficher l'étiquette de l'abscisse dans le graphique.
            st.info("###### Analyse graphique")
            df_trafic_st['Date'] = df_trafic_st.index

            # Calculer la tendance générale
            result = sm.OLS(df_trafic_st['Nombre de passages'], sm.add_constant(range(len(df_trafic_st)))).fit()
            df_trafic_st['Tendance'] = result.fittedvalues

            # Créer le graphique avec le comptage quotidien et la tendance
            fig_evo = px.line(df_trafic_st, x='Date', y=['Nombre de passages', 'Tendance'],
                          labels={'value': 'Nombre de passages et Tendance', 'Date': 'Jours (365) - 01/09/2022 au 31/08/2023'},
                          template='plotly_white',
                          height=600,
                          width=1000)
            fig_evo.update_layout(
                title='Evolution quotidienne du nombre de cyclistes captés par tous les sites',
                title_x=0.2)
            fig_evo.update_xaxes(dtick='M1')
            st.plotly_chart(fig_evo)

           # décomposition de la série temporelle en composants saisonniers, tendanciels et résiduels.
            
        
            st.write("###### Décomposition de la série temporelle en composants saisonniers, tendanciels et résiduels.")
            st.image("sarima1.JPG")

            st.write("D'après les graphiques ci-dessus, nous pouvons valider la présence de saisonnalité à la fois hebdomadaire (entre les jours de la semaine) et calendaire (hiver, été, vacances,… ) du nombre de cyclistes à Paris.")
            st.write("Cependant, étant donné le manque de données sur plusieurs années, il nous est difficile d'apprécier la tendance générale annuelle. Notons pour la suite de notre étude, la considération de la périodicité hebdomadaire de 7 jours.")

        elif (demarche == 'Analyse de stationnarité et test statistique'):

            st.info("###### Analyse de stationnarité et test statistique")
            st.write("Corrélogramme : ACF (Fonction d'Autocorrélation) et PACF (Fonction d'Autocorrélation Partielle) " )
            st.image("sarima2.JPG")
            st.write("L’analyse graphique de l'ACF montre que notre série temporelle n’est pas stationnaire. La décroissance lente des pics démontre cette caractéristique.")
            st.write("Cette observation est validée par le test statistique de Dickey-Fuller qui nous donne un p-value de 7,13% (> 5%). Ce qui n’a pas permis de rejeter l’hypothèse nulle qui signifie que la série est non stationnaire.")

        elif (demarche == 'Stationnarisation de la série'):

            st.info("###### Stationnarisation de la série")
            st.write("Afin de procéder à la modélisation, il est nécessaire de stationnariser notre série. Pour cela, nous avons effectué une différenciation d'ordre 2 pour éliminer la tendance quadratique dans notre série, et en intégrant une saisonalité de 7 jours. Nous obtenons ainsi les graphiques suivants.")

            st.image("sarima3.JPG")
            st.image("sarima4.JPG")

            st.write("Notre série est maintenant stationnaire. Le test statistique de Dickey-Fuller nous donne un p-value de 0.00 %. Ce qui a permis de rejeter l’hypothèse nulle indiquant ainsi que la série est stationnaire.")

        elif (demarche == 'Calcul et estimation des modéles'):
            st.info("###### Calcul et estimation des modéles")

            st.write("Nous avons pris comme jeu d'entrainement de notre modèle, la période allant de :blue[**01/09/2022 à 30/06/2023**], et comme jeu de test la période de :blue[**01/07/2023 au 31/08/2023**].")
            st.write("Pour déterminer les paramètres du modèle SARIMA, nous avons procédé à une itération des ordres p et q en calculant les métriques associées (AIC, BIC, RMSE et R2) . Pour les paramètres (d),(D), et (s) nous les avons fixés à 2,2 et 7. Ainsi, le résultat est récapitulé dans le tableau suivant :")
            # Créer un DataFrame exemple (remplacez ceci par vos propres données)
            st.write("")
            # img_param = Image.open("Metrique.png")
            # st.image(img_param, width = 700)

            # Affichage des métriques
            df_metric= pd.read_csv("metrique.csv", sep=';')

            # Convertir le DataFrame en une chaîne HTML avec alignement à droite et couleurs
            table_html = '<table style="text-align:right;">'
            table_html += '<tr>'
            for col in df_metric.columns:
                table_html += f'<th style="background-color: lightblue; padding: 10px;">{col}</th>'
            table_html += '</tr>'

            for _, row in df_metric.iterrows():
                table_html += '<tr>'
                for cell in row.values:
                    table_html += f'<td style="padding: 10px;">{cell}</td>'
                table_html += '</tr>'

            table_html += '</table>'

            # Afficher le tableau HTML avec st.markdown
            st.markdown(table_html, unsafe_allow_html=True)

        elif (demarche == 'Choix du modèle et présentation graphique'):
            st.info("###### Choix du modèle et présentation graphique")
            st.write("D’après le tableau des métriques précédent, le modèle ‘D’ avec les paramètres :blue[**(0,2,1)(0,2,1,7)**] nous donne le meilleur résultat en termes de RMSE et R2. En conséquence, nous avons donc choisi ce modèle pour effectuer nos prédictions sur notre jeu de test (juillet et août 2023).")
            # Affichage graphique de la prédiction et du réel (Juillet-Août 2023)
            @st.cache_data
            def load_data_pred():
                df_pred = pd.read_csv("df_pred.csv", sep=',')
                return df_pred

            df_pred = load_data_pred()

            fig_pred = px.line(df_pred, x='Date', y=['Nombre de passages', 'Prédiction'],
                          labels={'value': 'Nombre de passages et Tendance', 'Date': 'Jours (365) - 01/09/2022 au 31/08/2023'},
                          template='plotly_white',
                          height=600,
                          width=1000)
            fig_pred.update_layout(
                title='Evolution quotidienne du nombre de passages avec Prédiction du mois de juillet et août 2023',
                title_x=0.1)
            fig_pred.update_xaxes(dtick='M1')
            st.plotly_chart(fig_pred)
    
elif page == pages[5] :
    st.write("## **Conclusion et perspective**")
    
    st.write("Nous avons choisi le modèle de séries temporelles en raison des tendances, des saisons et des motifs temporels présents dans nos données, que les modèles basés sur des arbres pourraient avoir du mal à saisir. Il convient de noter que ce modèle offre une interprétation plus aisée, ce qui peut être avantageux dans certains contextes.")
    st.write("Cependant, des améliorations sont nécessaires pour notre modèle, notamment en raison du manque de données, ce qui rend difficile la capture de saisons plus longues telles que le cycle mensuel ou annuel. Il serait également pertinent d'explorer l'utilisation de modèles hybrides, combinant des approches basées sur des arbres avec du modèle des séries temporelles pour exploiter les forces de chaque méthode.")
    st.write("Enfin, il est recommandé d'évaluer régulièrement les performances du modèle à mesure que de nouvelles données deviennent disponibles, car les modèles de séries temporelles peuvent nécessiter une adaptation continue pour maintenir leur efficacité.")
    
    
































    
