import sqlite3
import pandas as pd
conn = sqlite3.connect('site12.db')
sql_query=pd.read_sql_query("select title,teamname from final",conn)
sql_query.to_csv(r'static/data.csv',index=False)
#sql_query.to_html("results.html")


# assign it to a
# variable (string)
