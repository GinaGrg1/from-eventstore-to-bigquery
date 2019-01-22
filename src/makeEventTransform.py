
def transform_quantity_moved_in_to_new_po(event_data):
    return transform_po_event(event_data)

def transform_etd_eta_changed(event_data):
    return transform_po_event(event_data)

def transform_purchase_order_approved(event_data):
    return transform_po_event(event_data)

def transform_none(event_data):
    event_data.pop("eventstore_timestamp", None)
    return event_data

def transform_po_event(data):
    new_data = {}
    for key, value in data.items():
        if key == 'delivery_schedule':
            dates = next(iter(value.values()))
            delivery_type = next(iter(value.keys())).split('_')[0]
            if 'eta' in dates:
                new_data['eta_date'] = dates.get('eta')
            if 'etd' in dates:
                new_data['etd_date'] = dates.get('etd')
            new_data['delivery_type'] = delivery_type
        else:
            new_data[key] = value
    return new_data
    

def get_transformer_for(event_type):
    event_type_mapping = {
        'quantity_moved_in_to_new_po': transform_quantity_moved_in_to_new_po,
        'etd_eta_changed': transform_etd_eta_changed,
        'purchase_order_approved': transform_purchase_order_approved,
    }
    return event_type_mapping.get(event_type, transform_none)






