# delete this later/sooner

supported_event_types = "quantity_moved_in_to_new_po,etd_eta_changed,purchase_order_approved"
event_types = supported_event_types.split(",")

def MakeEventTransform(event_type):
    transformer = get_transformer_for(event_type)
    return transformer


    for event in event_type:
        transformer = get_transformer_for(event_type)
        return 
        function_name = "transform_" + event 
        if (function_name in locals()):
            return locals()[function_name]
        else:
            return transform_none


