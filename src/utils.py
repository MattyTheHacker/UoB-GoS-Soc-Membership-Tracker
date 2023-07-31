import requests
import json
import os

from datetime import datetime

def get_all_data_file_names():
    # get all files in the data folder
    # we only want the json files
    # return a list of all the file names
    # remove the "combined.json" file as we don't want to include it
    path = "../data/json/"
    files = [filename for filename in os.listdir(path) if filename.endswith(".json")]
    # files.remove("combined.json")
    return files

def save_formatted_data(data, filename):
    with open(filename, 'x') as file:
        json.dump(data, file, indent=4)

def load_data_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def save_dictionary_to_file(dictionary, filename):
    # if it exits, overwrite it, otherwise create it
    with open(filename, 'w') as file:
        json.dump(dictionary, file, indent=4)

def load_dictionary_from_file(filename):
    with open(filename, 'r') as file:
        dictionary = json.load(file)
    return dictionary

def save_combined_to_csv():
    # get the combined.json file
    data = load_data_from_file("../data/json/combined.json")

    # get the dates
    dates = data["dates"]

    # get the socs
    socs = list(data.keys())

    # remove the dates from the socs
    socs.remove("dates")

    # create the csv file
    with open("../data/csv/combined.csv", 'w') as file:
        # write the header
        file.write("Society,")
        for date in dates:
            file.write(f"{date},")
        file.write("\n")

        # write the data
        for soc in socs:
            file.write(f"{soc},")
            for count in data[soc]:
                file.write(f"{count},")
            file.write("\n")

def get_data(url):
    response = requests.get(url)
    return response.json()

def get_generated_date(data):
    guild_dt = data["DateGenerated"]

    # convert to datetime object
    # current format: 2023-07-31T00:13:11.3832325+01:00
    # desired format: 2023-07-31T00:13:11
    # just take the first 19 characters
    guild_dt = guild_dt[:19]

    # remove colons
    guild_dt = guild_dt.replace(":", "")

    return guild_dt

def generated_date_to_datetime(date_generated):
    return datetime.strptime(date_generated, "%Y-%m-%dT%H%M%S")

def get_society_data():
    url = "https://www.guildofstudents.com/svc/voting/stats/election/membershipstats/112?groupIds=1&sortBy=itemname&sortDirection=ascending"
    data = get_data(url)
    date_generated = get_generated_date(data)
    save_formatted_data(data, f"../data/json/{date_generated}.json")

def combine_all_data():
    # we need to laod every datafile, and then combine them into one csv
    # the format of the data should be a dictionary in the format:
    # {society: [membership count 1, membership count 2, ...]}

    # get all the data from the json files
    data = {}

    # get all the file names
    files = get_all_data_file_names()

    # the first item in the dictionary should be a list of the dates the data was generated
    # we can get this from the file names
    dates = [file[:17] for file in files]

    # sort the dates
    dates.sort()

    # add the dates to the dictionary
    data["dates"] = dates

    # load the data from each file
    for file in files:
        # load the data from the file
        file_data = load_data_from_file(f"../data/json/{file}")

        # extract the data we want
        for society in file_data["Groups"][0]["Items"]:
            soc_name = society["Name"]
            soc_members = society["Eligible"]

            # check if this soc is already in the dictionary
            if soc_name in data:
                # the soc is already in the dictionary, so we need to append the new count to the list
                data[soc_name].append(soc_members)
            else:
                # the soc is not in the dictionary, so we need to add it
                data[soc_name] = [soc_members]

    # save the data to a json file
    save_dictionary_to_file(data, "../data/json/combined.json")

        
    

if __name__ == '__main__':
    get_society_data()
    combine_all_data()
    save_combined_to_csv()