# -*- coding: utf-8 -*-

import json
import unittest
import types

from makeEventTransform import get_transformer_for

class TestEventsTransformation(unittest.TestCase):
    def test_get_transformer_for(self):
        
        # Gets an event specific function if it exists 
        transform_etd = get_transformer_for('etd_eta_changed')
        self.assertEqual(transform_etd.__name__, 'transform_etd_eta_changed', "Function name does not match")
        self.assertEqual(isinstance(transform_etd, types.FunctionType), True, "{} is not a function".format(transform_etd))
        
        transform_po = get_transformer_for('purchase_order_approved')
        self.assertEqual(transform_po.__name__, 'transform_purchase_order_approved')
        self.assertEqual(isinstance(transform_po, types.FunctionType), True, "{} is not a function".format(transform_po))
        
        transform_qty_moved = get_transformer_for('quantity_moved_in_to_new_po')
        self.assertEqual(transform_qty_moved.__name__, 'transform_quantity_moved_in_to_new_po')
        self.assertEqual(isinstance(transform_qty_moved, types.FunctionType), True, "{} is not a function".format(transform_qty_moved))

        # Gets generic tranform fucntion if event specific function does not exist:
        transform = get_transformer_for('quantity_changed_exception')
        self.assertEqual(transform.__name__, 'transform_none')
        self.assertEqual(isinstance(transform, types.FunctionType), True, "{} is not a function".format(transform))

             
    def test_tranform_purchase_order_approved(self):
        transform_po = get_transformer_for('purchase_order_approved')
        
        purchase_test_data = self.open_json_file("./tests/files/sample_purchase_order_approved.json")
        purchase_order_data = transform_po(purchase_test_data)
        expected_po = self.open_json_file("./tests/files/expected_purchase_order.json")
        self.assertEqual(purchase_order_data, expected_po)
        
    def test_tranform_etd_eta_changed(self):
        
        transform_etd = get_transformer_for('etd_eta_changed')
        etd_test_data = self.open_json_file("./tests/files/sample_etd_eta_changed.json")
        etd_eta_data = transform_etd(etd_test_data)
        expected_etd_eta = self.open_json_file("./tests/files/expected_etd_eta.json")
        self.assertEqual(etd_eta_data, expected_etd_eta)
        

    def test_transform_quantity_moved_in_to_new_po(self):
       
        transform_qty_moved = get_transformer_for('quantity_moved_in_to_new_po')       
        quantity_test_data = self.open_json_file("./tests/files/sample_quantity_moved.json")
        quantity_moved_data = transform_qty_moved(quantity_test_data)
        expected_qty_moved = self.open_json_file("./tests/files/expected_quantity_moved.json")   
        self.assertEqual(quantity_moved_data, expected_qty_moved)
      
    def test_tranform(self):
        
        transform = get_transformer_for('quantity_changed_exception')
        test_data = self.open_json_file("./tests/files/sample_none.json")
        none_transformed = transform(test_data)
        expected_none_data = self.open_json_file("./tests/files/expected_none.json")     
        self.assertEqual(none_transformed, expected_none_data)
    
    def open_json_file(self, filename):
        with open(filename, "rb") as file:
            return json.load(file)
        

if __name__ == '__main__':
    unittest.main()
