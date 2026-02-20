import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    def categorize_delay(x):
        if x > 5:
            return "Late"
        elif x < -5:
            return "Early"
        else:
            return "On time"
        
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

st.title("Getaround Delay Analysis")
st.markdown(
    """
    This dashboard highlights the impact of late vehicle returns on Getaround.

    **It illustrates:**
    - the frequency and severity of delays,  
    - the consequences on conflicts between successive rentals,  
    - and the potential revenue loss for car owners.  

    **Goal**: help define the best buffer policy to reduce conflicts without sacrificing too much revenue.
    """
)

# Histogram 
with st.container():
    st.markdown("#### Distribution of Car Returns")
    st.caption("Most delays are concentrated around 0 → a large share of users return on time or with a slight delay. A few extreme cases extend the distribution.")
    fig_hist_delay = px.histogram(
        data_clean,
        x="delay_at_checkout_in_hours",
        labels={"delay_at_checkout_in_hours": "Delay at Check-out (minutes)"}
    )

    fig_hist_delay.add_vline(
        x=0,
        line_dash="dash",
        line_color="red",
        annotation_text="On time",
        annotation_position="top left"
    )

    fig_hist_delay.update_layout(
        xaxis_title="Return Delay (hours)",
        yaxis_title="Number of Rentals",
        bargap=0.05
    )

    fig_hist_delay.update_traces(xbins=dict(start=-24, end=24, size=0.25))
    st.plotly_chart(fig_hist_delay, use_container_width=True)

st.divider()

# Pie charte delay
col1, spacer, col2 = st.columns([4.75,0.5,4.75])
with col1.container():
    st.markdown("#### Proportion of Users On Time, Late, or Early")
    st.caption("A large share of rentals are returned on time, but nearly 52.8% show a significant delay.")
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
    st.markdown("#### Impact of Check-in Method on Delays")
    st.caption("“Mobile” users tend to accumulate more delays than “Connect” users, which may reflect a difference in usage.")
    fig_type_mean = px.bar(
        data_type_mean,
        x="checkin_type",
        y="delay_at_checkout_in_minutes"
    )
    st.plotly_chart(fig_type_mean, use_container_width=True)

st.divider()
with st.container():
    st.markdown("#### Which Buffer Effectively Reduces the Risk of Conflict?")
    st.caption("The longer the buffer, the lower the probability of conflict. However, this comes at the expense of revenue.")
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
        annotation_text="On time",
        annotation_position="top left"
    )
    st.plotly_chart(fig_buffer, use_container_width=True)
st.divider()
# Buffer slider 
with st.container():
    st.markdown("#### What Is the Effect of the Buffer Depending on the Check-in Type?")
    st.caption("The buffer reduces the risk of conflict, but the impact differs between “Mobile” and “Connect”.")
    buffer_h = st.slider(
            "Buffer Time (hours)",
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
        st.markdown("##### All")

        container, separator = st.columns([9.5,0.5])
        with container:
            st.metric("% Conflict", f"{row_all['conflict_percent']:.2f}%")
            st.metric("Number of Rentals Affected", f"{round(row_all['nbr_location_affect'])}")

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
            st.metric("% Conflict", f"{row_mobile['conflict_percent']:.2f}%")
            st.metric("Number of Rentals Affected", f"{round(row_mobile['nbr_location_affect'])}")
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
        st.metric("% Conflict", f"{row_connect['conflict_percent']:.2f}%")
        st.metric("Number of Rentals Affected", f"{round(row_connect['nbr_location_affect'])}")

st.divider()

# Buffer vs revenue
with st.container():
    st.markdown("#### What Is the Revenue Cost of an Overly Long Buffer?")
    st.caption("Each additional hour added to the buffer reduces the risk of conflict but also decreases the share of exploitable revenue.")
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
        st.markdown("The total amount of revenue that could be affected")
    with space_right:
        st.markdown("")

    fig_revene_potentialy_impact = px.line(
        data_impact_revenu_by_hours, 
        x="hours",
        y="revert_percentage",
        text="revert_percentage"
    )
    fig_revene_potentialy_impact.update_layout(
        xaxis_title="Hours",
        yaxis_title="Potential Percentage of Revenue Impact",
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
    st.markdown("#### What Happens When a Conflict Occurs?")
    st.caption(f"Only {percent_of_impact_data}% of the rentals in the dataset contain a back-to-back booking (one rental immediately followed by another). The indicators shown below are based only on this subset, since these are the only cases where a real conflict can be observed and measured.")
    left, center, right = st.columns(3)
    with left:
        container, separator = st.columns([9.5,0.5])
        with container:
            st.markdown("Proportion of Rentals Affected by a Delay")
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
            st.markdown("Share of Cancellations Directly Caused by a Delay")
            st.markdown(f"### {cancel_impact_percent}%")

        with separator:
            st.markdown("""
                <div class="separator-late"></div>
                """, unsafe_allow_html=True)
    with right:
        st.markdown("Average Waiting Time in Case of Conflict")
        st.markdown(f"### {mean_late_positive}")

    fig_impact_late = px.histogram(
        data_impact_late[data_impact_late['late_impact'].between(0, 24)],
        x="late_impact",
        nbins=100,
    )
    fig_impact_late.update_layout(
        xaxis_title="Delay Duration Causing a Conflict (hours)",
        yaxis_title="Number of Affected Rentals",
    )
    st.plotly_chart(fig_impact_late, use_container_width=True)

st.markdown(
    """
    #### Conclusion:
    The analysis shows that delays impact around 8.6% of potential revenue.  

    - Introducing a buffer significantly reduces conflicts between successive rentals.  
    - On the other hand, each additional buffer hour leads to a progressive loss of potential revenue (up to 8.6%).  

    This dashboard allows exploring different scenarios to identify the best trade-off between conflict reduction and revenue preservation.
    """
)