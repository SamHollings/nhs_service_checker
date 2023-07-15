"""
This is the entrypoint for the repo - running this script will:
- get the list of NHS services [ToDo]
- check their website links work [ToDo]
- for each service:
    - check they have a CQC widget on their website [ToDo]

Need to:
- implement config
- implement logging
- implement saving API calls to a database, to avoid need for repeated calls
"""

# this part imports our Python packages, including our project's modules
import logging
import timeit 
from pathlib import Path
import json
import requests
import pandas as pd
# from src.utils.data_connections import read_sql_file, get_df_from_server, make_database_connection
from src.utils.file_paths import get_config
# from src.utils.logging_config import configure_logging 
# from src.processing.clean import calculate_years, process_columns
# from src.processing.derive_fields import gp_count_by_region, calculate_mean_years

logger = logging.getLogger(__name__)

def main():
    """"""
    # # load config, here we load our project's parameters from the config.toml file
    # config = get_config("config.toml") 
    # server = config ['server']
    # database = config['database']
    # schema = config['schema']
    # table = config['table']
    # filled_value = config['filled_value']
    # output_dir = Path(config['output_dir'])
    # log_dir = Path(config['log_dir'])

    # configure logging
    # configure_logging(log_dir, config)
    # logger.info(f"Configured logging with log folder: {log_dir}.")

    ########################################################################
    # Get the list of GP practices from the NHS.UK API
    ########################################################################

    NHS_API_SUBSCRIPTION_KEY = get_config("secret.toml")['nhs_api_subscription_key']


    def get_nhs_service_details(nhs_api_subscription_key):
        """"""
        response = requests.request(
            method='POST',
            url='https://api.nhs.uk/service-search/search?api-version=1',
            headers={
                'Content-Type': 'application/json',
                'subscription-key': nhs_api_subscription_key
            },
            #"filter": "(OrganisationTypeID eq 'DEN') or (OrganisationTypeID eq 'GPB') or (OrganisationTypeID eq 'GPP')"
            data='''
                    {
                        "filter": "(OrganisationTypeID eq 'DEN') or (OrganisationTypeID eq 'GPP')",
                        "orderby": "OrganisationName",
                        "top": 25,
                        "skip": 0,
                        "count": true
                    }
                        ''',
            timeout=60)

        if response.status_code == 200:
            data = response.json()

            return pd.DataFrame(data["value"])

        else:
            print("Error occurred. Status code:", response.status_code)
            return []

    # Call the function to retrieve the nhs service data
    df_nhs_service_details = get_nhs_service_details(NHS_API_SUBSCRIPTION_KEY)

    # Print the retrieved GP practices
    for index,organisation in df_nhs_service_details.iterrows():
        
        print(organisation)

        #print(f"Name: {organisation['']}\nAddress: {organisation['']}\n")
        break

    
    def get_cqc_data(org_id):
        """"""
        #ToDo: Need to figure how to link the CQC output to the Organisation code of the org - I can't think of how to do this besides just pulling ALL of the 
        #       CQC data and then getting the org codes for each org using the locations/{location_id} API... but it seems overkill. Perhaps there is some query parameter..
        url = f'https://api.cqc.org.uk/public/v1/locations'
        req = requests.get(url)
        return (req.json())

    # # sets up database connection
    # conn = make_database_connection(server, database)

    # # load data, this part handles importing our data sources     
    # query = read_sql_file('sql', 'example.sql', database, schema, table)
    # gp_df = get_df_from_server(conn, server, database, query)

    # # follow pre-processing steps  
    # gp_df.rename(columns={'ADDRESS_LINE_5': 'REGION', 
    #                    'OPEN_DATE': 'OPENED', 
    #                    'CLOSE_DATE': 'CLOSED'}, inplace=True)
    
    # gp_df = process_columns(gp_df, 
    #     date_col_names = ['OPENED', 'CLOSED'], 
    #     string_col_names= ['REGION', 'NAME']
    #     )

    # gp_df = calculate_years(filled_value, gp_df)
        
    # # prepare data for CSV
    # publication_breakdowns = {}
    # publication_breakdowns['gp_data'] = gp_df

    # # follow data processing steps
    # region_df = gp_count_by_region(gp_df)
    # region_df = calculate_mean_years(region_df, gp_df)

    # publication_breakdowns['region_data'] = region_df

    # # produce outputs
    # for table_name, df in publication_breakdowns.items():
    #     df.to_csv(output_dir / f'{table_name}.csv', index=False)
    #     logger.info('\n\n%s.csv created!\n', table_name)
    # logger.info(f"Produced output(s) in folder: {output_dir}.")
    
if __name__ == "__main__":
    print(f"Running create_publication script")
    start_time = timeit.default_timer()
    main()
    total_time = timeit.default_timer() - start_time
    print(f"Running time of create_publication script: {int(total_time / 60)} minutes and {round(total_time%60)} seconds.\n")
