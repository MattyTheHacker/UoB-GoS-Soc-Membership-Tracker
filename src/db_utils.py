import sqlite3
import os

def save_to_database(data, date_generated):
    # takes in a json of new society data, extract the date, society names and membership counts
    # and save them to the database
    # for each new data pull, we need to add a new column for the date
    # we also need to add a new row for each society
    # the format of the data should be a dictionary in the format:
    # {society: [membership count 1, membership count 2, ...]}
    db_file_path = "../data/database/society_data.db"

    # put the society names and membership counts into a dictionary
    socs = {}
    for society in data["Groups"][0]["Items"]:
        socs[society["Name"]] = society["Eligible"]

    # check if the database exists, if not, create it
    if not os.path.exists(db_file_path):
        print("Database doesn't seem to exist... creating it now")

    conn = sqlite3.connect(db_file_path)
    cur = conn.cursor()

    # check if the table exists, if not, create it
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='society_data'")

    if cur.fetchone() is None:
        # the table doesn't exist, so we need to create it
        print("Table doesn't seem to exist... creating it now")
        cur.execute("CREATE TABLE society_data (society_name TEXT PRIMARY KEY)")

    # check if the date column exists, if not, create it
    cur.execute("PRAGMA table_info(society_data)")

    # get the column names
    columns = [column[1] for column in cur.fetchall()]

    if date_generated not in columns:
        # the date column doesn't exist, so we need to create it
        print("Date column doesn't seem to exist... creating it now")
        cur.execute(f"ALTER TABLE society_data ADD COLUMN '{date_generated}' INTEGER")

    # check if the socs are already in the database
    cur.execute("SELECT society_name FROM society_data")
    socs_in_db = [soc[0] for soc in cur.fetchall()]

    # if the society is already in the db, simply put the data into the new column
    # if it isn't, we need to add a new row for it
    for soc in socs:
        if soc in socs_in_db:
            # the soc is already in the db, so we need to update it
            command = "UPDATE society_data SET '{0}' = ? WHERE society_name = ?".format(date_generated)
            try:
                cur.execute(command, (socs[soc], soc))
            except Exception as e:
                print("[ERROR] Couldn't execute the following command: ")
                print(command)
                print(e)
        else:
            command = "INSERT INTO society_data (society_name, '{0}') VALUES (?,?)".format(date_generated)
            try: 
                cur.execute(command, (soc, socs[soc]))
            except Exception as e:
                print("[ERROR] Couldn't execute the following command: ")
                print(command)
                print(e)
                


    # commit the changes
    conn.commit()

    # close the connection
    conn.close()


