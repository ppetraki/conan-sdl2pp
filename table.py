#!/usr/bin/env python3

import yaml


class ConanOption:
    def __init__(self, name, dictionary):
        self.name = name
        self.default = dictionary.get('default')
        self.description = dictionary.get('description')
        self.ctype = dictionary.get('type')
        self.cmake_key = dictionary.get('cmake_key')

    def __str__(self):
        out_type = None
        if self.ctype == 'boolean':
            out_type = '[True, False]'
        elif self.ctype == 'int':
            out_type = 'Integer'
        elif self.ctype == 'string':
            out_type = 'ANY'
        else:
            raise Exception("unsupported type")

        line_template = '|{0}    | {1} |  {2} | {3} |'
        return line_template.format(self.name, self.default, out_type, self.description)


if __name__ == '__main__':
    with open('config.yaml', 'r') as config_file:
        options = yaml.load(config_file, Loader=yaml.FullLoader)

        # print(yaml.dump(options))

        header = '''
### Available Package Options
| Option        | Default | Possible Values  | Description
|:------------- |:-----------------  |:----------------- |:------------|
'''
        with open('table.md', 'w+') as out:
            out.write(header)
            for k, v in options['options'].items():
                out.write(str(ConanOption(k, v)))
                out.write('\n')
