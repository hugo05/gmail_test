from db import DB

from utils import Utils
from email_action import EmailAction

def main():
    
    queries = Utils.load_conditions_json()
    conditions = queries.get("conditions")
    
    for condition in conditions:
        
        query = Utils.create_query(condition.get("get_conditions"))
        res = DB.get_data(query, ())
        if res:
            Utils.make_email_modifications(condition, res)
        else:
            print("No results found for the given conditions")
        
        



if __name__ == "__main__":
    main()