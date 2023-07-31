import utils

if __name__ == '__main__':
    # Upate the data
    utils.get_society_data()

    # Combine the data
    utils.combine_all_data()

    # Create the csv
    utils.save_combined_to_csv()
    
    