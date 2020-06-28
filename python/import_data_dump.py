import json

data_in = {}
data_out = {'tables': {}}
table_ids = {}
field_ids = {}
errors = set()
bad_field_ids = set()
with open("alca.json") as f:
    data_in = json.load(f)
for thing in data_in['definition']:
    for table in thing['table']:
        data_out['tables'][table['$']['name']] = {
            'table_id': table['$']['tid'],
            'fields': table['field'],
            'records': []
        }
        # add table_id: table_name to table_ids 
        table_ids[table['$']['tid']] = table['$']['name']
        # add field_id: field_name to field_ids
        for field in table['field']:
            field_ids[field['$']['fid']] = field['$']['name']

# copy rows from data_in to data_out and format
for thing in data_in['data']:
    for table in thing['t']:
        for record in table['record']:
            # add record to table in data_out in format field_name: field_value
            record_out = {}
            for field in record['f']:
                if field["$"]['fid'] in field_ids:
                    record_out[field_ids[field["$"]['fid']]] = field["_"]
                else:
                    errors.add(f'Skipping field id {field["$"]["fid"]} with value {field["_"]} because it does not exist in the table definition.\n')
            data_out['tables'][table_ids[table['$']['tid']]]['records'].append(record_out)

# check for fields that share "name"
for table in data_out['tables']:
    for field in data_out['tables'][table]['fields']:
        count = 0
        field_names = field_ids.values()
        for i in range(len(field_names)):
            if field['$']['name'] == list(field_names)[i]:
                count = count + 1
        if count > 1:
            errors.add(f'Multiple fields named {field["$"]["name"]}.\n')

with open('output.json', 'w') as f:
    json.dump(data_out, f, sort_keys=True, indent=4)
with open('errors.txt', 'w') as f:
    errors = list(errors)
    errors.sort()
    f.writelines(errors)
