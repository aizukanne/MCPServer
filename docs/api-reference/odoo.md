# Odoo ERP Integration

These tools provide integration with an Odoo ERP system.

## `odoo_get_mapped_models`

Get a list of available Odoo models.

- **Parameters:**
  - `include_fields` (boolean, optional): Whether to include model fields in the response.
  - `model_name` (string, optional): The name of a specific model to get.
- **Returns:**
  - A JSON object containing a list of models.

## `odoo_fetch_records`

Retrieve records from an Odoo model.

- **Parameters:**
  - `external_model` (string): The name of the Odoo model.
  - `filters` (list, optional): A list of filters to apply to the search.
- **Returns:**
  - A JSON object containing a list of records.

## `odoo_create_record`

Create a new record in an Odoo model.

- **Parameters:**
  - `external_model` (string): The name of the Odoo model.
  - `record_data` (dict): The data for the new record.
- **Returns:**
  - A JSON object containing the ID of the new record.

## `odoo_update_record`

Update an existing record in an Odoo model.

- **Parameters:**
  - `external_model` (string): The name of the Odoo model.
  - `record_id` (integer): The ID of the record to update.
  - `**fields` (dict): The fields to update.
- **Returns:**
  - A JSON object confirming the update.

## `odoo_delete_record`

Delete a record from an Odoo model.

- **Parameters:**
  - `external_model` (string): The name of the Odoo model.
  - `record_id` (integer): The ID of the record to delete.
- **Returns:**
  - A JSON object confirming the deletion.

## `odoo_print_record`

Generate a PDF report for a record.

- **Parameters:**
  - `model_name` (string): The name of the Odoo model.
  - `record_id` (integer): The ID of the record.
- **Returns:**
  - A JSON object containing the PDF report.

## `odoo_post_record`

Post a record, triggering a workflow action.

- **Parameters:**
  - `external_model` (string): The name of the Odoo model.
  - `record_id` (integer): The ID of the record.
- **Returns:**
  - A JSON object confirming the action.