import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import nltk
from collections import Counter

def groupchat(filename):
    with open(filename, encoding="utf-8") as f:
        return f.read()

chat = groupchat("Bestiezz.txt")

date_pattern = r'\d+/\d+/\d+'  # the date pattern
all_dates = re.findall((date_pattern), chat)  # filter out all dates
msg_dates = []  # to store the dates for messages messages alone
non_msg_dates = []  # to store the dates for actions
sender_msg = re.split((date_pattern), chat)  # remove the date from the chats, left with only users and messages
sender = []  # to store users
msg = []  # to store messages alone
time = []  # to store time message was sent
nonMatch = []  # to store actions...
count = 0
for item in sender_msg:
    matchObj = re.match(r', (.*) - (.*): (.*)', item, re.DOTALL)
    if matchObj:
        msg_dates.append(all_dates[count - 1])
        time.append(matchObj.group(1))
        sender.append(matchObj.group(2))
        msg.append(matchObj.group(3))
    else:
        non_msg_dates.append(all_dates[count])
        nonMatch.append(item)
    count = count + 1


numpy_data = np.array([msg_dates, time, sender, msg])
numpy_data = numpy_data.transpose()
df = pd.DataFrame(numpy_data, columns=["Date", "Time", "User", "Message"])
df = df[~df.Message.str.contains("<Media omitted>")]

most_active_user = df.User.value_counts()
most_active_date = df.Date.value_counts()

most_active_user[:6].plot(kind='bar')
plt.xlabel('Users')
plt.ylabel('Messages')
plt.suptitle('Bestiezz')
plt.show()
most_active_date[:10].plot(kind='bar')
plt.show()

df['characters'] = df.Message.apply(len)
df['words'] = df.Message.apply(lambda x: len(x.split()))

a = df.groupby('User').mean().sort_values('characters').round(2)
print("LONGEST MESSAGE")
print(a[:6])

b = df.Message.value_counts().head(20)
print('COMMON MESSAGE')
print(b)

words = ''
for i in df.Message.values:
    words += '{} '.format(i.lower()) # make words lowercase

c = pd.DataFrame(Counter(words.split()).most_common(70), columns=['word', 'frequency'])
print('COMMON WORDS')
print(c)
