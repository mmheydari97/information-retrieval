# open terminal from project location where you can see manage.py
# type python manage.py shell
# then exec these codes line by line in the new shell
import pandas as pd
from search import models
import re
from datetime import datetime

path = "IR-F19-Project02-14k.csv"
# path = "IR-F19-Project01-Input-2k.xlsx"
date_pattern = r"(\w*)\s(\d{1,2})\w{2}\s(\d{4}),\s(\d{2}:\d{2}:\d{2})"
prog = re.compile(pattern=date_pattern)
# df = pd.read_excel(path)
# df = pd.read_csv(path)

# This should be commented out at last to use the whole dataset
###############################
# df = df[:10]  # ###############
###############################

# This populates the database
# for row in df.iterrows():
#     parts = prog.match(row[1]["publish_date"]).groups()
#     f_date = "{} {} {} {}".format(parts[0], parts[1], parts[2], parts[3])
#     news = models.News(
#         doc_id=row[0],
#         publish_date=datetime.strptime(f_date, "%B %d %Y %H:%M:%S"),
#         title=row[1]["title"],
#         url=row[1]["url"],
#         summary=row[1]["summary"],
#         meta_tags=row[1]["meta_tags"],
#         content=row[1]["content"],
#         thumbnail=row[1]["thumbnail"]
#     )
#     news.save()
#     print(news.doc_id)

for df in pd.read_csv(path, chunksize=1000):
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

