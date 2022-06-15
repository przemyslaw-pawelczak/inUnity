class Metadata:
    """
    AST node for LLVM metadata
    """

    elements = {}

    def __init__(self, name, metadata_type, metadata_function_name, values, includes):
        self.name = name
        self.type = metadata_type
        self.type_name = metadata_function_name
        # values can be a dictionary or a list. each element can be a string, a reference to other metadata or a Metadata object.
        self.values = values
        self.includes = includes

        if self.name is not None:
            self.elements[self.name] = self


    def __str__(self):
        return '{} = {}(includes: {}; values: {})'.format(self.name, self.type_name, self.includes, self.values)


    @staticmethod
    def fancy_format(metadata):
        """
        Formats the metadata and returns it
        """

        retval = ''

        if 'line' in metadata:
            retval += 'Line: {}; '.format(metadata['line'])
        
        if 'column' in metadata:
            retval += 'Column: {}; '.format(metadata['column'])
        
        if 'variable_name' in metadata:
            retval += 'Variable name: {}; '.format(metadata['variable_name'])
                
        if 'subprogram_name' in metadata:
            retval += 'Function name: {}; '.format(metadata['subprogram_name'])

        if 'file' in metadata:
            retval += 'File: {}; '.format(metadata['file'])

        if retval[-2:] == '; ':
            retval = retval[:-2]

        return retval


    def retrieve(self):
        """
        Resolve metadata tree and return only relevant metadata information
        """

        if len(self.values) == 0 and len(self.includes) == 0:
            return {}

        if self.type_name == 'DIFile':
            return {'file': '{}/{}'.format(self.values['directory'], self.values['filename'])}

        if self.type_name == 'DILocation':
            # retrieve scope
            retrived_vals = self.elements[self.values['scope']].retrieve()

            return {**retrived_vals, **{'line': self.values['line'], 'column': self.values['column']}}

        if self.type_name == 'DISubprogram':
            # get file name
            file = self.elements[self.values['file']].retrieve()
            
            return {**file, **{'subprogram_name': self.values['name']}}

        if self.type_name == 'DILexicalBlock':
            # retrieve scope
            retrived_vals = self.elements[self.values['scope']].retrieve()

            if 'file' not in retrived_vals:
                retrived_vals['file'] = self.elements[self.values['file']].retrieve()['file']

            return retrived_vals

        if self.type_name == 'DILocalVariable':
            # retrieve scope
            retrived_vals = self.elements[self.values['scope']].retrieve()

            try:
                return {**retrived_vals, **{'variable_name': self.values['name'], 'line': self.values['line'], 'column': self.values['column']}}
            except Exception:
                return {**retrived_vals, **{'variable_name': self.values['name'], 'line': self.values['line']}}
        
        location = None
        local_var = None

        # find the element that contains the relevant metadata informations.
        for i in self.includes:

            # empty DIExpression()
            if i == 'empty':
                return None

            if self.elements[i].type_name == 'DILocation':
                location = i
            if self.elements[i].type_name == 'DILocalVariable':
                local_var = i

        # Local Variable has higher priority (contains more information)
        # NB: is only for local variable declarations
        if local_var is not None:
            return self.elements[local_var].retrieve()

        # If the metadata is not associated with local variable
        # or DILocalVariable not found, use DILocation
        if location is not None:
            return self.elements[location].retrieve()
