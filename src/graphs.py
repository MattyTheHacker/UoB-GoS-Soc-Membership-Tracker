import utils
import matplotlib.pyplot as plt

def graph_all_societies():
    # get all the data from the combined json
    # the data is in the format:
    # {"dates": [date 1, date 2, ...]"}
    # {society: [membership count 1, membership count 2, ...]}
    # x labels will be the dates

    # get the data
    data = utils.load_dictionary_from_file("../data/json/combined.json")

    x_label = "Date Generated"
    y_label = "Number of Members"
    title = "Number of Members in Societies Over Time"

    # get the x and y values - this is broke now
    for k, v in data.items():
        plt.plot(range(1, len(v) + 1), v, '.-', label=k)

    plt.legend()

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def graph_top_x_societies(x):
    data = utils.load_dictionary_from_file("../data/json/combined.json")

    x_label = "Date Generated"
    y_label = "Number of Members"
    title = "Number of Members in Societies Over Time"

    # use the dates as the x labels
    dates = data["dates"]
    data.pop("dates")

    # convert to datetime objects
    dates = [utils.generated_date_to_datetime(date) for date in dates]

    # convert the dates to format: DD/MM/YYYY HH:MM:SS
    dates = [date.strftime("%d/%m/%Y %H:%M:%S") for date in dates]

    # set the x labels with the date on the top line and the time on the bottom line
    x_labels = [f"{date[:10]}\n{date[11:]}" for date in dates]

    # set the x ticks
    plt.xticks(range(1, len(x_labels) + 1), x_labels, rotation=45)

    # convert dictionary to list of tuples
    data = [(k, v) for k, v in data.items()]

    # sort the data by the last value in the tuple
    sorted_data = sorted(data, key=lambda x: x[1][-1], reverse=True)

    # get the top x societies
    top_x = sorted_data[:x]

    # get the x and y values
    for k, v in top_x:
        plt.plot(range(1, len(v) + 1), v, '.-', label=k)

    plt.legend()

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    # plt.show()

    plt.savefig(f"../graphs/top_{x}_societies.svg", format='svg', dpi=300)


def graph_society(society_name):
    # get all data
    data = utils.load_dictionary_from_file("../data/json/combined.json")

    # remove the dates from the data and set them as the x labels
    dates = data["dates"]
    data.pop("dates")

    # convert to datetime objects
    dates = [utils.generated_date_to_datetime(date) for date in dates]

    # convert the dates to format: DD/MM/YYYY HH:MM:SS
    dates = [date.strftime("%d/%m/%Y %H:%M:%S") for date in dates]

    # set the x labels with the date on the top line and the time on the bottom line
    x_labels = [f"{date[:10]}\n{date[11:]}" for date in dates]

    # set the x ticks
    plt.xticks(range(1, len(x_labels) + 1), x_labels, rotation=45)

    # get the data for the society
    society_data = data[society_name]

    # get the x and y values
    x = range(1, len(society_data) + 1)
    y = society_data
    
    x_label = "Date Generated"
    y_label = "Number of Members"
    title = f"Number of Members in {society_name} Over Time"

    plt.plot(x, y, '.-')
    plt.legend()

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # plt.show()
    plt.savefig(f"../graphs/{society_name}.svg", format='svg', dpi=300)



if __name__ == '__main__':
    # graph_all_societies()
    graph_society("Computer Science Society (CSS)")

    graph_top_x_societies(10)