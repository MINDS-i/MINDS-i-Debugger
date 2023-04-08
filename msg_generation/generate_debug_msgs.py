#!/usr/bin/env python
import argparse
from copy import deepcopy
from jinja2 import Environment, FileSystemLoader
import os
import yaml

# mapping from a c type to the corresponding python struct format
TYPE_TO_STRUCT_FORMAT = dict(
    char='c',
    uint8_t='B',
    int8_t='b',
    uint16_t='H',
    int16_t='h',
    uint32_t='I',
    int32_t='i'
)

class DebugMsgGenerator:
    def __init__(self, config_file, templates_dir, skip_timestamps):
        self.templates_dir = templates_dir
        self.config_data = yaml.safe_load(open(config_file, 'r'))

        if not skip_timestamps:
            stamped_debug_msgs = []
            for debug_msg in self.config_data['debug_msgs']:
                stamped_debug_msg = deepcopy(debug_msg)
                stamped_debug_msg['name'] = f"stamped_{stamped_debug_msg['name']}"
                # Add 10 to the stamped ID 0x10 becomes 0x1A
                try:
                    stamped_debug_msg['id'] = f"0x{int(stamped_debug_msg['id'], 16) + 10:X}"
                except:
                    raise ValueError(f"{debug_msg['name']} has an invalid ID: {debug_msg['id']}")
                stamped_debug_msg['fields'] = [
                    dict(
                        name='timestamp',
                        struct_type='uint32_t',
                        num_format='.3',
                        interpret=dict(
                            type='float',
                            func='ms_to_s'),
                        description='Arduino time (ms) when the message was created')] + \
                    stamped_debug_msg['fields']
                stamped_debug_msgs.append(stamped_debug_msg)

            interleaved_list = []
            for debug_msg, stamped_debug_msg in zip(self.config_data['debug_msgs'], stamped_debug_msgs):
                interleaved_list += [debug_msg, stamped_debug_msg]
            self.config_data['debug_msgs'] = interleaved_list

        # check to make sure all msg_ids are valid and unique
        msg_ids = {}
        for debug_msg in self.config_data['debug_msgs']:
            try:
                msg_id = int(debug_msg['id'], 16)
            except:
                raise ValueError(f"{debug_msg['name']} has an invalid ID: {debug_msg['id']}")
            if msg_id < 0 or msg_id > 255:
                raise ValueError(f"{debug_msg['name']} has an out of range ID: {debug_msg['id']}")
            if msg_id in msg_ids.keys():
                raise ValueError(f"{debug_msg['name']} and {msg_ids[msg_id]} have the same ID: {debug_msg['id']}")
            msg_ids[msg_id] = debug_msg['name']

        self.built_in_type_to_size = self.config_data['built_in_types']
        self.custom_type_to_fields = self.config_data['custom_types']

        self.env = Environment(loader = FileSystemLoader(self.templates_dir), trim_blocks=True, lstrip_blocks=True)
        self.env.filters['to_camel_case'] = self.to_camel_case
        self.env.filters['get_msg_len'] = self.get_msg_len
        self.env.filters['get_type_size'] = self.get_type_size
        self.env.filters['handle_field'] = self.handle_field
        self.env.filters['get_base_types'] = self.get_base_types
        self.env.filters['get_struct_format'] = self.get_struct_format
        self.env.filters['get_print_format'] = self.get_print_format
        self.env.filters['get_interpreted_value'] = self.get_interpreted_value
        self.env.filters['get_field_description'] = self.get_field_description
    
    def generate_source(self):
        for template in os.listdir(self.templates_dir):
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src')
            if '.py.' in template:
                output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
            elif '.md.' in template:
                output_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            with open(os.path.join(output_dir, template.rsplit('.', maxsplit=1)[0]), 'w') as f:
                f.write(self.env.get_template(template).render(self.config_data))

    def get_print_format(self, field):
        if field['struct_type'] in self.built_in_type_to_size.keys():
            interpreted_type = field.get('interpret', {}).get('type', field['struct_type'])
            format_str = str(field.get('num_format', ''))
            if interpreted_type == 'float':
                format_str += 'f'
            else:
                format_str += 'd'
            yield f"{{{''.join(self.get_interpreted_value(field))}:{format_str}}}"
        else:
            interpreted_type = field.get('interpret', {}).get('type', None)
            if interpreted_type is not None:
                format_str = str(field.get('num_format', ''))
                if interpreted_type == 'float':
                    format_str += 'f'
                else:
                    format_str += 'd'
                yield f"{{{''.join(self.get_interpreted_value(field))}:{format_str}}}"
            else:
                for sub_field in self.custom_type_to_fields[field.get('cast_type', field['struct_type'])]:
                    yield from self.get_print_format(self, sub_field)

    def get_interpreted_value(self, field):
        if field['struct_type'] in self.built_in_type_to_size.keys():
            interpret = field.get('interpret', None)
            if interpret is not None:
                yield f"{field['interpret']['func']}({field['name']})"
            else:
                yield field['name']
        else:
            interpret = field.get('interpret', None)
            if interpret is not None:
                yield f"{field['interpret']['func']}({', '.join([sf['name'] for sf in self.get_base_types(field)])})"
            else:
                for sub_field in self.custom_type_to_fields[field.get('cast_type', field['struct_type'])]:
                    yield from self.get_interpreted_value(sub_field)

    def get_base_types(self, field):
        if field.get('cast_type', field['struct_type']) in self.built_in_type_to_size.keys():
            yield field
        else:
            for sub_field in self.custom_type_to_fields[field.get('cast_type', field['struct_type'])]:
                for base_type in self.get_base_types(sub_field):
                    renamed_base_type = deepcopy(base_type)
                    renamed_base_type['name'] = '_'.join([field['name'], base_type['name']])
                    yield renamed_base_type

    def handle_field(self, field, first=False, prepend=''):
        if field.get('cast_type', field['struct_type']) in self.built_in_type_to_size.keys():
            for i in range(self.built_in_type_to_size[field.get('cast_type', field['struct_type'])]):
                input_str = f"{'msg.' if first else ''}{prepend}{self.to_camel_case(field['name'], first=False)}"
                if 'mod_offset' in field:
                    input_str = f"({input_str} + {field['mod_offset']})"
                if 'mod_factor' in field:
                    input_str = f"{input_str} * {field['mod_factor']}"
                if 'cast_type' in field:
                    if field['struct_type'] == 'float':
                        input_str = f"{field['cast_type']}(round({input_str}))"
                    else:
                        input_str = f"{field['cast_type']}({input_str})"
                if i == 0:
                    yield f'{input_str} & 0xFF'
                else:
                    yield f'{input_str} >> {i * 8}'
        else:
            for type_field in self.custom_type_to_fields[field.get('cast_type', field['struct_type'])]:
                input_prepend = f"{'msg.' if first else ''}{prepend}{self.to_camel_case(field['name'], first=False)}."
                for string in list(self.handle_field(type_field, prepend=input_prepend)):
                    yield string

    def get_field_description(self, field, name_prepend='', descr_prepend=''):
        if field.get('cast_type', field['struct_type']) in self.built_in_type_to_size.keys():
            # caclulate field range and resolution given transmission type
            field_bits = self.get_type_size(field.get('cast_type', field['struct_type'])) * 8
            if 'u' in field.get('cast_type', field['struct_type']):
                # unsigned
                field_min = 0.0
                field_max = 2**field_bits
            else:
                field_min = -2**(field_bits - 1)
                field_max = 2**(field_bits - 1) - 1
            field_resolution = 1.0 / field.get('mod_factor', 1.0)
            field_min *= field_resolution
            field_max *= field_resolution
            field_offset = field.get('mod_offset', 0.0)
            field_min -= field_offset
            field_max -= field_offset

            if field['struct_type'] == 'float':
                field_min = f"{field_min:.6}"
                field_max = f"{field_max:.6}"
                field_resolution = f"{field_resolution:.3}"
            else:
                field_min = f"{int(field_min):d}"
                field_max = f"{int(field_max):d}"
                field_resolution = f"{int(field_resolution):d}"
            yield (name_prepend + field['name'],
                   self.get_type_size(field.get('cast_type', field['struct_type'])),
                   field_min, field_max, field_resolution,
                   descr_prepend + field.get('description', 'TBD'))
        else:
            for sub_field in self.custom_type_to_fields[field.get('cast_type', field['struct_type'])]:
                yield from self.get_field_description(
                    sub_field,
                    name_prepend=f"{field['name']}.",
                    descr_prepend=f"{field.get('description', 'TBD')} ")
    
    def get_struct_format(self, type):
        return (TYPE_TO_STRUCT_FORMAT[type], 'B' * self.get_type_size(type), self.get_type_size(type))

    def get_type_size(self, type_name):
        if type_name in self.built_in_type_to_size.keys():
            return self.built_in_type_to_size[type_name]
        else:
            type_len = 0
            for type_field in self.custom_type_to_fields[type_name]:
                type_len += self.get_type_size(type_field.get('cast_type', type_field['struct_type']))
            return type_len
    
    def get_msg_len(self, msg):
        msg_len = 0
        for field in msg['fields']:
            msg_len += self.get_type_size(field.get('cast_type', field['struct_type']))
        return msg_len

    def to_camel_case(self, string, first=True):
        return ''.join([s.capitalize() if (i > 0 or first) else s for i, s in enumerate(string.split('_'))])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-timestamps', action='store_true',
                        help='Flag to skip generation of a stamped version of each message '\
                             '(by default, stamped messages are generated)')
    args = parser.parse_args()

    config_file = os.path.join(os.path.dirname(__file__), 'debug_msgs.yaml')
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    dmg = DebugMsgGenerator(config_file=config_file,
                            templates_dir=templates_dir,
                            skip_timestamps=args.skip_timestamps)
    dmg.generate_source()
