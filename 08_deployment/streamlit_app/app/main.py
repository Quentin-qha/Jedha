import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    def categorize_delay(x):
        if x > 5:
            return "retard"
        elif x < -5:
            return "avance"
        else:
            return "À l'heure"
        
    def add_scope(df_scope, scope_name):
        n_total = len(df_scope)
        for h in range(-24, 25):
            n_conflicts = (df_scope['delay_at_checkout_in_hours'] > h).sum()
            pct = round(100 * n_conflicts / n_total, 2) if n_total else 0.0
            conflict_percent_results.append({
                "buffer_hours": h,
                "conflict_percent": pct,
                "nbr_location_affect": int(n_conflicts),
                "type": scope_name
            })

    df = pd.read_excel("data/get_around_delay_analysis.xlsx")
    data_clean = df[(df["delay_at_checkout_in_minutes"].between(-1440, 1440))].copy()
    data_clean = data_clean[data_clean['state'] == "ended"]
    data_clean = data_clean.drop(columns=['car_id', 'rental_id', 'previous_ended_rental_id'])

    data_clean['delay_at_checkout_in_hours'] = data_clean['delay_at_checkout_in_minutes'] / 60

    data_clean["delay_category"] = data_clean["delay_at_checkout_in_minutes"].apply(categorize_delay)
    delay_counts = data_clean["delay_category"].value_counts().reset_index()
    delay_counts.columns = ["category", "count"]

    data_type_mean = data_clean.groupby("checkin_type")["delay_at_checkout_in_minutes"].mean().reset_index()

    conflict_percent_results = []
    add_scope(data_clean, "all")
    add_scope(data_clean[data_clean['checkin_type'] == "mobile"], "mobile")
    add_scope(data_clean[data_clean['checkin_type'] == "connect"], "connect")
    data_buffer = pd.DataFrame(conflict_percent_results).sort_values(by="buffer_hours").reset_index()

    data_impact_late =  df[df["time_delta_with_previous_rental_in_minutes"].notna()].copy()
    data_impact_late =  data_impact_late[data_impact_late["delay_at_checkout_in_minutes"].notna()]
    data_impact_late["late_impact"] = round((data_impact_late["delay_at_checkout_in_minutes"] - data_impact_late["time_delta_with_previous_rental_in_minutes"])/60,2)

    mean_late_positive = round(data_impact_late.loc[data_impact_late["late_impact"] > 0, "late_impact"].mean(),2)
    mean_late_hours = int(mean_late_positive)
    mean_late_minutes = int((mean_late_positive % 1) * 60)
    mean_late_positive = f"{mean_late_hours}h{mean_late_minutes:02d}min"
    reel_impact_percent = round((len(data_impact_late[data_impact_late['late_impact'] > 0])/len(data_impact_late))*100,2)
    
    percent_of_impact_data = round(len(data_impact_late)/len(df)*100, 2)

    data_late_canceled =  df[df["time_delta_with_previous_rental_in_minutes"].notna()].copy()
    data_canceled = data_late_canceled[data_late_canceled["state"] == "canceled"]
    data_canceled = data_canceled[data_canceled['time_delta_with_previous_rental_in_minutes']>0]
    cancel_impact_percent = round(len(data_canceled)/len(data_late_canceled[data_late_canceled["state"] == "canceled"])*100,2)

    potentially_affected = df[df["previous_ended_rental_id"].notna()].copy()
    potentially_affected_count = len(potentially_affected)
    revenue_potentially_affected = potentially_affected_count / len(df) * 100
    potentially_affected["time_delta_with_previous_rental_in_hours"] = potentially_affected["time_delta_with_previous_rental_in_minutes"]/60

    hour_impacted_revenue = []
    for h in range(0,15):
        data_hour_revenue_count = len(potentially_affected[potentially_affected["time_delta_with_previous_rental_in_hours"]>=h])
        data_revenu_percentage_by_hour = round(data_hour_revenue_count / len(df)*100,2)
        hour_impacted_revenue.append(
            {
                "hours": h,
                "percentage": data_revenu_percentage_by_hour
            }
        )
    data_impact_revenu_by_hours = pd.DataFrame(hour_impacted_revenue)
    data_impact_revenu_by_hours["revert_percentage"] = round(revenue_potentially_affected - data_impact_revenu_by_hours["percentage"],2)


    return data_clean, delay_counts, data_type_mean, data_buffer, data_impact_late, mean_late_positive, reel_impact_percent, cancel_impact_percent, percent_of_impact_data, revenue_potentially_affected, data_impact_revenu_by_hours

data_clean, delay_counts, data_type_mean, data_buffer, data_impact_late, mean_late_positive, reel_impact_percent, cancel_impact_percent, percent_of_impact_data, revenue_potentially_affected, data_impact_revenu_by_hours = load_data()

st.title("Analyse des retards Getaround")
st.markdown(
    """
    Ce tableau de bord met en lumière l’impact des retards de restitution des véhicules sur Getaround.

    **Il illustre à la fois :**
    - la fréquence et la gravité des retards,
    - les conséquences sur les conflits entre locations successives,
    - et la perte potentielle de revenus pour les propriétaires.

    **Objectif** : aider à définir la meilleure politique de buffer pour réduire les conflits sans sacrifier trop de revenu.
    """
)

# Histogram 
with st.container():
    st.markdown("#### Distribution des restitutions des voitures")
    st.caption("La majorité des retards se concentrent autour de 0 → une grande partie rend à l’heure ou avec un léger retard. Quelques cas extrêmes allongent la distribution.")
    fig_hist_delay = px.histogram(
        data_clean,
        x="delay_at_checkout_in_hours",
        labels={"delay_at_checkout_in_hours": "Retard au check-out (minutes)"}
    )

    fig_hist_delay.add_vline(
        x=0,
        line_dash="dash",
        line_color="red",
        annotation_text="À l'heure",
        annotation_position="top left"
    )

    fig_hist_delay.update_layout(
        xaxis_title="Délai au retour (heures)",
        yaxis_title="Nombre de locations",
        bargap=0.05
    )

    fig_hist_delay.update_traces(xbins=dict(start=-24, end=24, size=0.25))
    st.plotly_chart(fig_hist_delay, use_container_width=True)

st.divider()

# Pie charte delay
col1, spacer, col2 = st.columns([4.75,0.5,4.75])
with col1.container():
    st.markdown("#### Proportion d’utilisateurs ponctuels, en retard ou en avance")
    st.caption("Une part importante des locations est rendue à l’heure, mais près de X% présentent un retard significatif.")
    fig_delay_pie = px.pie(
        delay_counts,
        names="category",
        values="count",
    )
    st.plotly_chart(fig_delay_pie, use_container_width=True)
with spacer:
    st.markdown("")
# Count par type de checkin
with col2.container():
    st.markdown("#### Impact du mode de check-in sur les retards")
    st.caption("Les utilisateurs “mobile” semblent accumuler plus de retard que les utilisateurs “connect”, ce qui peut refléter une différence d’usage.")
    fig_type_mean = px.bar(
        data_type_mean,
        x="checkin_type",
        y="delay_at_checkout_in_minutes"
    )
    st.plotly_chart(fig_type_mean, use_container_width=True)

st.divider()
with st.container():
    st.markdown("#### Quel buffer réduit efficacement le risque de conflit ?")
    st.caption("Plus le buffer est long, plus la probabilité de conflit diminue. Mais cela se fait au détriment du revenu.")
    fig_buffer = px.line(
        data_buffer,
        x="buffer_hours",
        y="conflict_percent",
        color="type",
    )
    fig_buffer.add_vline(
        x=0,
        line_dash="dash",
        line_color="red",
        annotation_text="À l'heure",
        annotation_position="top left"
    )
    st.plotly_chart(fig_buffer, use_container_width=True)
st.divider()
# Buffer slider 
with st.container():
    st.markdown("#### Quel est l’effet du buffer selon le type de check-in ?")
    st.caption("Le buffer réduit le risque de conflit, mais l’impact varie entre “mobile” et “connect”.")
    buffer_h = st.slider(
            "Délais du buffer (heures)",
            min_value=int(data_buffer["buffer_hours"].min()),
            max_value=int(data_buffer["buffer_hours"].max()),
            value=0
        )
    data_buffer_all = data_buffer[data_buffer["type"] == "all"]
    row_all = data_buffer_all[data_buffer_all["buffer_hours"] == buffer_h].iloc[0]

    data_buffer_mobile = data_buffer[data_buffer["type"] == "mobile"]
    row_mobile = data_buffer_mobile[data_buffer_mobile["buffer_hours"] == buffer_h].iloc[0]

    data_buffer_connect = data_buffer[data_buffer["type"] == "connect"]
    row_connect = data_buffer_connect[data_buffer_connect["buffer_hours"] == buffer_h].iloc[0]

    st.markdown("<br>", unsafe_allow_html=True)
    
    left, center, right = st.columns(3)
    with left:
        st.markdown("##### Tous")

        container, separator = st.columns([9.5,0.5])
        with container:
            st.metric("% Conflit", f"{row_all['conflict_percent']:.2f}%")
            st.metric("Nombre de locations impactées", f"{round(row_all['nbr_location_affect'])}")
        with separator:
            st.markdown("""
                <style>
                .vline-full {
                border-left: 1px solid #31333f33;
                height: 160px;
                margin: 0 auto;
                }
                </style>
                <div class="vline-full"></div>
                """, unsafe_allow_html=True)

    with center:
        st.markdown("##### Mobile")

        container, separator = st.columns([9.5,0.5])
        with container:
            st.metric("% Conflit", f"{row_mobile['conflict_percent']:.2f}%")
            st.metric("Nombre de locations impactées", f"{round(row_mobile['nbr_location_affect'])}")
        with separator:
            st.markdown("""
                <style>
                .vline-full {
                border-left: 1px solid #31333f33;
                height: 160px;
                margin: 0 auto;
                }
                </style>
                <div class="vline-full"></div>
                """, unsafe_allow_html=True)

    with right:
        st.markdown("##### Connect")
        st.metric("% Conflit", f"{row_connect['conflict_percent']:.2f}%")
        st.metric("Nombre de locations impactées", f"{round(row_connect['nbr_location_affect'])}")

st.divider()
# Buffer vs revenue
with st.container():
    st.markdown("#### Quel est le coût en revenu d’un buffer trop long ?")
    st.caption("Chaque heure ajoutée au buffer réduit les risques de conflit mais diminue aussi la part de revenu exploitable.")
    spacer_left, left, right, space_right = st.columns([2, 1.5, 3, 2])
    with spacer_left:
        st.markdown("")
    with left:
        st.markdown("""
                <style>
                .padding-revenue_left {
                height: 0px;
                margin: 0 auto;
                position: relative;
                }
                .padding-revenue_left::before{
                    content: "";
                    width: 24rem;
                    height: 5.3rem;
                    background-color: #FFFFFF;
                    position: absolute;
                    top: 1.5rem;
                    left: -1.5rem;
                    border-radius: 1rem;
                }
                </style>
                <div class="padding-revenue_left"></div>
                """, unsafe_allow_html=True)
        st.markdown(f"## {round(revenue_potentially_affected,2)}%")
    with right:
        st.markdown("""
                <style>
                .padding-revenue_right {
                height: 24px;
                margin: 0 auto;
                }
                </style>
                <div class="padding-revenue_right"></div>
                """, unsafe_allow_html=True)
        st.markdown("Le nombre total de revenu qui pourraient être affectés")
    with space_right:
        st.markdown("")
    #st.divider()

    #st.caption("Dans ce graphique vous pourrez voir le potentiel de location perdue (et donc leur revenus) sur la totalité des locations")

    fig_revene_potentialy_impact = px.line(
        data_impact_revenu_by_hours, 
        x="hours",
        y="revert_percentage",
        text="revert_percentage"
    )
    fig_revene_potentialy_impact.update_layout(
        xaxis_title="Heures",
        yaxis_title="Pourcentage potentiel d'impact sur le revenu",
        bargap=0.05
    )
    fig_revene_potentialy_impact.update_traces(
        textposition="top center",
        texttemplate="%{text}%"
    )
    st.plotly_chart(fig_revene_potentialy_impact, use_container_width=True)
st.divider()
#with st.container(border=True):
with st.container():
    st.markdown("#### Que se passe-t-il quand un conflit survient ?")
    st.caption(f"Seules {percent_of_impact_data}% des locations du dataset contiennent un enchaînement de réservations (une location suivie immédiatement d’une autre). Les indicateurs présentés ci-dessous s’appuient uniquement sur ce sous-ensemble, car ce sont les seuls cas où un conflit réel peut être observé et mesuré.")
    left, center, right = st.columns(3)
    with left:
        container, separator = st.columns([9.5,0.5])
        with container:
            st.markdown("Proportion de locations affectées par un retard")
            st.markdown(f"### {reel_impact_percent}%")

        with separator:
            st.markdown("""
                <style>
                .separator-late {
                border-left: 1px solid #31333f33;
                height: 120px;
                margin: 0 auto;
                }
                </style>
                <div class="separator-late"></div>
                """, unsafe_allow_html=True)
    with center:
        container, separator = st.columns([9.5,0.5])
        with container:
            st.markdown("Part des annulations directement dues à un retard")
            st.markdown(f"### {cancel_impact_percent}%")

        with separator:
            st.markdown("""
                <div class="separator-late"></div>
                """, unsafe_allow_html=True)
    with right:
        st.markdown("Durée moyenne de l’attente en cas de conflit")
        st.markdown(f"### {mean_late_positive}")

    fig_impact_late = px.histogram(
        data_impact_late[data_impact_late['late_impact'].between(0, 24)],
        x="late_impact",
        nbins=100,
    )
    fig_impact_late.update_layout(
        xaxis_title="Durée du retard causant un conflit (heures)",
        yaxis_title="Nombre de locations concernées"
    )
    st.plotly_chart(fig_impact_late, use_container_width=True)

st.markdown(
    """
    #### Conclusion :
    L’analyse montre que les retards impactent environ 8,6% du revenu potentiel.

    - L’instauration d’un buffer réduit significativement les conflits entre locations successives.
    - En contrepartie, chaque heure de buffer représente une perte progressive de revenu potentiel (jusqu’à 8,6%).

    Ce dashboard permet d’explorer différents scénarios afin d’identifier le meilleur compromis entre réduction des conflits et préservation du revenu.
    """
)