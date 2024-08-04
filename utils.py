import json
from email_action import EmailAction

class Utils:

	@staticmethod
	def load_conditions_json():
		file_path = 'conditions.json'
		with open(file_path, 'r') as file:
		    data = json.load(file)
		return data

	
	@staticmethod
	def fetch_date_query(condition):

	    predicate = condition.get("predicate")
	    unit = condition.get("unit")
	    unit_val = int(condition.get("unit_val"))

	    if unit == "day":
	        return """ date {} datetime('now', '-{} days')""".format(predicate, unit_val)
	    elif unit == "month":
	        return  """ date {} datetime('now', '-{} months')""".format(predicate, unit_val)
	    else:
	        raise Exception("Invalid unit passed")

	
	@staticmethod
	def create_sender_query(condition):

		predicate = condition.get("predicate")

		if predicate == "contain":
		    return " sender LIKE '%{}%'".format(condition.get("value")) 
		elif predicate == "not_contain":
		    return " sender NOT LIKE '%{}%'".format(condition.get("value"))
		elif predicate == "equal":
		    return " sender = '{}'".format(condition.get("value"))
		elif predicate == "not_equal":
		    return " sender != '{}'".format(condition.get("value"))
		else:
		    raise Exception("Invalid predicate passed")

	
	@staticmethod
	def create_recipient_query(condition):

		predicate = condition.get("predicate")

		if predicate == "contain":
		    return " recipients LIKE '%{}%'".format(condition.get("value")) 
		elif predicate == "not_contain":
		    return " recipients NOT LIKE '%{}%'".format(condition.get("value"))
		elif predicate == "equal":
		    return " recipients LIKE '%{}%'".format(condition.get("value"))
		elif predicate == "not_equal":
		    return " recipients NOT LIKE '%{}%'".format(condition.get("value"))
		else:
		    raise Exception("Invalid predicate passed")


	@staticmethod
	def create_subject_query(condition):

		predicate = condition.get("predicate")

		if predicate == "contain":
		    return " subject LIKE '%{}%'".format(condition.get("value")) 
		elif predicate == "not_contain":
		    return " subject NOT LIKE '%{}%'".format(condition.get("value"))
		elif predicate == "equal":
		    return " subject LIKE '%{}%'".format(condition.get("value"))
		elif predicate == "not_equal":
		    return " subject NOT LIKE '%{}%'".format(condition.get("value"))
		else:
		    raise Exception("Invalid predicate passed")


	@staticmethod
	def create_body_query(condition):

		predicate = condition.get("predicate")

		if predicate == "contain":
		    return " body LIKE '%{}%'".format(condition.get("value")) 
		elif predicate == "not_contain":
		    return " body NOT LIKE '%{}%'".format(condition.get("value"))
		elif predicate == "equal":
		    return " body LIKE '%{}%'".format(condition.get("value"))
		elif predicate == "not_equal":
		    return " body NOT LIKE '%{}%'".format(condition.get("value"))
		else:
		    raise Exception("Invalid predicate passed")
	
	
	@staticmethod
	def create_query(condition):
        
		query = """SELECT id FROM Emails WHERE """

		q_predicate = "" if len(condition.keys()) < 3 else "AND" if condition.get("all") else "OR" 

		date_cond = condition.get("date")
		if date_cond:
		    qry = Utils.fetch_date_query(date_cond)
		    query = query + qry

		sender = condition.get("sender")
		if sender:
		    qry = Utils.create_sender_query(sender)
		    query = query + " " + q_predicate + qry

		recipients = condition.get("recipients")
		if recipients:
		    qry = Utils.create_recipient_query(recipients)
		    query = query + " " + q_predicate + qry

		subject = condition.get("subject")
		if subject:
		    qry = Utils.create_subject_query(subject)
		    query = query + " " + q_predicate + qry

		body = condition.get("body")
		if body:
		    qry = Utils.create_body_query(body)
		    query = query + " " + q_predicate + qry

		return query


	@staticmethod
	def make_email_modifications(condition, results):
		modification = condition.get("modification")
		if modification:
			read_unread = modification.get("read_unread")
			move = modification.get("move")


			for result in results:
				mail_id = result[0]

				if read_unread:
					EmailAction.mark_email_read_unread(result[0], read_unread.get("mark_read"))
				if move:
					EmailAction.move_email(mail_id, move.get("destination"))
		else:
			print("No modifications provided for the given conditions")

