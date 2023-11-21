import pandas as pd
import time
import random

random.seed()

while True:
    time.sleep(1)
    with open("quote_request.txt", "r+") as quote_request:
        quote_data = quote_request.read().split()
        df = pd.read_excel('quote_collection.xlsx')
        
        if quote_data[0] == "Topic": 
            spec_topic = quote_data[1]
            topic_df = df[df["Topic"] == spec_topic]
            random_num = random.randint(1, 10000)
            random_row = random_num % topic_df.shape[0]
            selected_quote = topic_df.iloc[random_row]
            quote_request.seek(0)
            quote_request.truncate(0)
            quote_request.write("None")
            with open("quote_sent.txt", "w") as quote_sent:
                quote_sent.write(str(selected_quote["Quote"]) + " - " + str(selected_quote["From"]))

        elif quote_data[0] == "Medium":
            spec_medium = quote_data[1]
            medium_df = df[df["Medium"] == spec_medium]
            random_num = random.randint(1, 10000)
            random_row = random_num % medium_df.shape[0]
            selected_quote = medium_df.iloc[random_row]
            quote_request.seek(0)
            quote_request.truncate(0)
            quote_request.write("None")
            with open("quote_sent.txt", "w") as quote_sent:
                quote_sent.write(str(selected_quote["Quote"]) + " - " + str(selected_quote["From"] + " From " + str(selected_quote["Title"])))
        
        elif quote_data[0] == "Random":
            random_num = random.randint(1, 10000)
            random_row = random_num % df.shape[0]
            selected_quote = df.iloc[random_row]
            quote_request.seek(0)
            quote_request.truncate(0)
            quote_request.write("None")
            with open("quote_sent.txt", "w") as quote_sent:
                if str(selected_quote["Title"]) != "nan":
                    quote_sent.write(str(selected_quote["Quote"]) + " - " + str(selected_quote["From"] + " From " + str(selected_quote["Title"])))
                else: 
                    quote_sent.write(str(selected_quote["Quote"]) + " - " + str(selected_quote["From"]))