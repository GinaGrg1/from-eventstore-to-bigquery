
import pickle

event_list = pickle.load(open("event_list.p","rb"))


supported_event_types = "quantity_moved_in_to_new_po,etd_eta_changed,purchase_order_approved"

new_list = [(event_type, event_data)for event_type, event_data in event_list if event_type in supported_event_types]
print(new_list)

pickle.dump(new_list, open("clean_list.p","wb"))