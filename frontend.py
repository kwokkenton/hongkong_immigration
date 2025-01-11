import streamlit as st



conn = st.connection("neon", type="sql")
# Perform query.
df = conn.query('SELECT * FROM passengers;', ttl="10m")
# Print results.
# st.markdown("[]
st.write("""# Is Hong Kong facing Depopulation?

![Photo by Ryan McManimie on Unsplash](https://miro.medium.com/v2/resize:fit:720/format:webp/0*H1MD2lTwgxdPAAaX)

All data belongs to their respective owners.

The past several years have been particularly challenging for Hong Kong, but the decisive blow was dealt by the National Security Law (NSL), which made many residents seriously consider leaving permanently.

I have definitely heard more Cantonese being spoken on the streets of London and Manchester, and have seen more social media groups popping up offering a helping hand to new immigrants. 

Recently, there have been new schemes to attract Hong Kongers to travel to the mainland for consumption, entertainment, as well as work.

Quantifying how many people that plan to leave or have left is a difficult task. But what is the trend?

Bloomberg Opinion have looked at proxies such as the withdrawal of money from the Mandatory Provident Fund and the application for certificates of no criminal conviction, which have all increased. What I am interested in is Immigration data.

""")

st.write("""## Most frequently used control points
There are 15 control points in Hong Kong. 
""")
df_freq_arrivals = df[['control_point','arrivals', 'departures']].groupby(['control_point']).sum().sort_values('arrivals', ascending = True)
st.bar_chart(df_freq_arrivals, stack=False)
st.write("""## Most frequently used control points
""")
df_identity = df[['identity', 'arrivals', 'departures']].groupby(['identity']).sum()
st.bar_chart(df_identity, stack=False)
st.write("""## Time series
""")
df['flux'] = df.arrivals-df.departures
st.bar_chart(df,x='date',y='flux', stack=False)

