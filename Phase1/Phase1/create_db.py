# Run these in a manage.py shell
import pandas as pd
from search import models
import re
from datetime import datetime

path = "News.xlsx"
date_pattern = r"(\w*)\s(\d{1,2})\w{2}\s(\d{4}),\s(\d{2}:\d{2}:\d{2})"
prog = re.compile(pattern=date_pattern)
df = pd.read_excel(path)

# This should be commented out
###############################
df = df[:10]  # ###############
###############################

for row in df.iterrows():
    parts = prog.match(row[1]["publish_date"]).groups()
    f_date = "{} {} {} {}".format(parts[0], parts[1], parts[2], parts[3])
    news = models.News(
        doc_id=row[0],
        publish_date=datetime.strptime(f_date, "%B %d %Y %H:%M:%S"),
        title=row[1]["title"],
        url=row[1]["url"],
        summary=row[1]["summary"],
        meta_tags=row[1]["meta_tags"],
        content=row[1]["content"],
        thumbnail=row[1]["thumbnail"]
    )
    news.save()
