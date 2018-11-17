"""
###Aca va ejemplos de como se debe armar json
Columnas personalizadas # Aca va explicacion y ejemplo de las columas personalizadas
'concat':
'detail':
'delete':
'link':
"""
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from dashboard.tools import ToolsBackend as Tools


def convert(data, header=None, table_attributes=None, custom_column=None, actual_page=None, attributes_column=None,
            multi_header=None, footer=None):
    # Genera la etiqueta <table> con sus atributos
    obj_generate_table = GenerateTableList(table_attributes=table_attributes)  # Se inicia la clase y definen atributos
    # de la tabla

    obj_generate_table._multi_header = multi_header

    if type(data) is dict and 'results' in data:  # Si la data no tiene el elemento "results" se setea "None" para
        # eliminar errores de compilacion
        data_table = data['results']
    elif type(data) is list:
        data_table = data
    else:
        data_table = None

    # Genera el cuerpo de la tabla
    # Construye el cuerpo hasta el cierre de la etiqueta </table>
    html_output = obj_generate_table.convert(data_table, header, custom_column, attributes_column, footer)

    # Genera el paginador, Si envian pagina actual y data tiene el total de paginas
    if actual_page and type(data) is dict and 'total_pages' in data:  # Si envia la cantidad de paginas para el listado
        html_output += obj_generate_table.pagination(count_pages=data['total_pages'], actual_page=actual_page)

    return html_output


def get_actual_page(request):
    if 'page' in request.GET:
        actual_page = request.GET['page']
    else:
        actual_page = 1
    return actual_page


class GenerateTableList(object):
    _multi_header = None
    _acum = {}
    """
    Class that manages the conversion of a Duple to a string of HTML.

    """

    def __init__(self, table_attributes=None):
        table_attributes_defaul = {"class": "table table-striped table-bordered table-hover "}

        if table_attributes is not None and not isinstance(table_attributes, dict):
            raise TypeError("Table attributes must be either a `dict` or `None`.")
        if table_attributes:
            table_attributes_defaul = self.merge_atributes(default=table_attributes_defaul, custom=table_attributes)

        self._table_opening_tag = "<table{:s}>".format(
            GenerateTableList._dict_to_html_attributes(table_attributes_defaul))

    def convert(self, data_list, header, custom_column, attributes_column, footer):
        """
        Funcion principal de la clase para crear tablas dinamicas
        :param data_list:
        :param header:
        :param custom_column:
        :param attributes_column:
        :param footer:
        :return:
        """

        html_output = "<div class='overflow-auto'>"
        html_output += self._table_opening_tag
        if self._multi_header:
            headers_tabla = self._multi_header
        else:
            headers_tabla = header

        html_output += self._markup_header_row(headers_tabla)

        if data_list:
            html_output += "<tr>"
            for row_data in data_list:
                for (field, key) in header:  # key es el identificar de la columna
                    if custom_column and key in custom_column:
                        custom_value = self.create_custom_value(custom_column[key], row_data)
                        value = custom_value
                    elif key in row_data.keys() and row_data[key]:
                        value = row_data[key]
                    else:
                        value = ""

                    html_output += self.create_table_data(value, key, attributes_column)

                    if footer:
                        self.accumulate_values(row_data, key, footer)
                html_output += "</tr>"

            if footer:
                html_output += self.get_footer(footer, header)

        else:
            html_output += "<tr><td colspan='{}'>{}</td></tr>".format(len(header), _("search is empty").title())
        html_output += "</table></div>"
        return html_output

    @staticmethod
    def create_table_data(value, key=None, attributes_column=None):
        attrs = ""
        if type(attributes_column) is dict and key in attributes_column:
            for attr_name in attributes_column[key]:
                attrs += "{}='{}'".format(attr_name, attributes_column[key][attr_name])

        return "<td {attrs}>{value}</td>".format(value=value, attrs=attrs)

    def get_footer(self, footer, header):
        html_output = ''

        for row in footer:
            html_output += '<tr>'
            for (field, key) in header:
                value = ''
                if key in row:
                    value = self.get_footer_value(row, key, footer)

                html_output += self.create_table_data(value)
            html_output += '</tr>'
        return html_output

    def get_footer_value(self, row, key, footer=None):
        data = row[key]
        value = ''

        if data['type'] == 'acum':
            value = 0
            for acum in self._acum[key]:
                value += float(self._acum[key][acum])

        if data['type'] == 'eval':
            f = footer
            value = eval(data['data'])  # Esto debe ser string como "int(r['num'])-1"

        if 'format_price' in data:
            tools = Tools()
            value = tools.format_to_decimal(value)

        row.update({'_' + key: value})  # Guarda el valor para la columna y posicione del footer

        return value

    def accumulate_values(self, row_data, key, footer):
        """
        Funcion creada para acumular o guardar en un dict los valores de una columna
        """

        for f in footer:

            if key in f and f[key]['type'] == 'acum':

                if key not in self._acum:
                    self._acum[key] = {}  # Si no existe todavia ese acumulador, se define como dict

                self._acum[key].update({row_data[f[key]['id']]: row_data[f[key]['value']]})

    def create_custom_value(self, custom_column_data, row_data=None):
        value = ""
        type_colum = custom_column_data['type']
        data = custom_column_data['data']

        if type_colum == 'concat':
            texts = []
            separator = ""  # Separador entre los String concatenados
            if 'separator' in custom_column_data:
                separator = custom_column_data['separator']

            for key_column in data:

                if row_data and key_column in row_data:  # Si la columna existe en la data enviada
                    if type(data) is dict:  # Si la data es un dict, recorremos recursivamente den elemento padre
                        custom_column_data_aux = {'type': type_colum, 'data': data[key_column], 'separator': separator}
                        recursion = self.create_custom_value(custom_column_data_aux, row_data[key_column])
                        texts.append(str(recursion))
                    else:
                        texts.append(str(row_data[key_column]))

                elif row_data and type(key_column) is str:  # Si el valor es un simple string, se guarda
                    texts.append(str(key_column))

            value = separator.join(texts)  # Se crea un solo string de la lista, separadas por el separador definido

        if type_colum == 'detail':
            #  Columna estandar para mostrar icono de ir al detalle
            value += '<a href="{}"><i class="fa fa-search"></i></a>'.format(
                reverse(data['url'], args=(row_data[data['key']],)))

        if type_colum == 'delete':
            #  Columna estandar para mostrar icono de borrar
            value += '<i class="fa fa-trash pointer color-red ico-delete-row" data-url="{}" data-id="{id}"></i>'.format(
                reverse(data['url']), id=row_data[data['key']])

        if type_colum == 'submit':
            #  Columna estandar para mostrar boton sutmit personalizado
            if 'name' in data:
                name = data['name']
            else:
                name = ""
            if 'key' in data and data['key'] in row_data :
                key = row_data[data['key']]  # Key debe ser el id que identifica la fila
            else:
                key = ""
            if 'cls' in data:
                cls = data['cls']
            else:
                cls = ""
            if 'text' in data:
                text = data['text']
            else:
                text = ""
                
            value += '<button name="{name}" type="submit" value="{val}" class="{cl}">{text}</button>'\
                    .format(name=name, val=key, cl=cls, text=text)


        if type_colum == 'link':
            """"
            Caso para crear links personalizados, con parametros y argumentos
            
            Requerido: data['text'], data['url']
            data['text']: Define el texto a mostrar en el listadao
            data['url']: nombre de la url
            data['arguments']: define argumentos tipo get e.g. ?client=69            
            data['key']: define valor a pasar en la funcion reverse

            """
            arguments = ''

            if 'arguments' in data:
                arguments += '?'
                data_arg = data['arguments']
                for arg_key in data_arg:
                    if row_data and data_arg[arg_key] in row_data:
                        argument_value = row_data[data_arg[arg_key]]
                    else:
                        argument_value = data_arg[arg_key]
                    arguments += '{param}={value}'.format(param=arg_key, value=argument_value)

            if 'key' in data:
                url = reverse(data['url'], args=(row_data[data['key']],))
            else:
                url = reverse(data['url'])

            value += '<a href="{url}{arg}">{text}</i></a>'.format(url=url, arg=arguments, text=data['text'])

        if type_colum == 'date':
            tools = Tools()

            date = data[0]
            if row_data and date in row_data:
                date = row_data[data[0]]

            value = tools.date_format_to_view(date=date)

        if type_colum == 'datetime':
            tools = Tools()

            date = data[0]
            if row_data and date in row_data:
                date = row_data[data[0]]

            value = tools.datetime_format_to_view(date=date)

        if type_colum == 'format_price':
            tools = Tools()

            number = data[0]
            if row_data and number in row_data:
                number = row_data[data[0]]

            value = tools.format_to_decimal(number)

        if type_colum == 'eval':
            r = row_data
            value = eval(data[0])  # Esto debe ser string como "int(r['num'])-1"

        if type_colum == 'if_eval':
            r = row_data
            condition = eval(data[0])  # Esto debe ser string como "int(r['num'])>1"
            
            if not condition:  # Eval retorna string
                custom_column_data = dict(
                    custom_column_data)  # Se crea una copia de si mismo para no afectar otras columnas
                custom_column_data.pop('next', None)  # Eliminamos next por no cumplir con la condicion
                
                if 'next_elif' in custom_column_data: # en caso quiera hacer algo sino cumplio condicion
                    custom_column_data['next'] = custom_column_data['next_elif']

        if 'next' in custom_column_data:
            next_custom_colum = custom_column_data['next']

            if 'data' not in next_custom_colum:
                next_custom_colum['data'] = (value,)

            value = self.create_custom_value(next_custom_colum, row_data)

        return value

    def _markup_header_row(self, headers):

        """
        Creates a row of table header items.

        Parameters
        ----------
        headers : list
            List of column headers. Each will be wrapped in `<th></th>` tags.
        
        Returns
        -------
        str
            Table row of headers.
        """

        html_output = ''

        if type(headers[
                    0]) is list:  # Si el primer registro es una lista, se usa funcion recursiva para traer multi head
            for h in headers:
                html_output += self._markup_header_row(h)

            return html_output

        html_output = "<tr>"
        for (key, data) in headers:
            rowspan = '1'
            colspan = '1'

            if type(data) is dict:
                if 'rowspan' in data:
                    rowspan = data['rowspan']
                if 'colspan' in data:
                    colspan = data['colspan']

            html_output += "<th rowspan='{rs}' colspan='{cs}'>{text}</th>"\
                .format(text=self.capitalize(key), rs=rowspan, cs=colspan)
        html_output += "</tr>"

        return html_output

    @staticmethod
    def capitalize(line):
        if len(line) <= 0:
            return ''
        return line[0].upper() + line[1:]

    @staticmethod
    def _dict_to_html_attributes(d):
        """
        Converts a dictionary to a string of ``key=\"value\"`` pairs.
        If ``None`` is provided as the dictionary an empty string is returned, 
        i.e. no html attributes are generated.

        Parameters
        ----------
        d : dict
            Dictionary to convert to html attributes.

        Returns
        -------
        str
            String of HTML attributes in the form ``key_i=\"value_i\" ... key_N=\"value_N\"``, 
            where ``N`` is the total number of ``(key, value)`` pairs.  
        """
        if d is None:
            return ""

        return "".join(" {}=\"{}\"".format(key, value) for key, value in iter(d.items()))

    @staticmethod
    def merge_atributes(default, custom):
        if 'class' in custom:
            default['class'] += custom['class']

        return dict(custom, **default)

    @staticmethod
    def pagination(count_pages, actual_page):
        left_class = right_class = ''
        left_type = right_type = 'submit'
        page = int(actual_page)

        pagination_html = '<div class="aling-right"><div class="pagination">'
        if page <= 1:
            left_class = 'disable'
            left_type = 'button'

        pagination_html += '<button type="{t}" name="page" value="1" class="p-btn p-left-start {cl}"></button>'\
            .format(t=left_type, cl=left_class)

        pagination_html += '<button type="{t}" name="page" value="{val}" class="p-btn p-left {cl}"></button>'.format(
            val=int(page) - 1, cl=left_class, t=left_type)

        pagination_html += '<spam>{p} {page} {of} {count}</spam>'\
            .format(page=page, count=count_pages, p=_('page').title(), of=_('of'))

        if page >= count_pages:
            right_class = 'disable'
            right_type = 'button'
        pagination_html += '<button type="{t}" name="page" value="{val}" class="p-btn p-right {cl}"></button>'.format(
            val=int(page) + 1, cl=right_class, t=right_type)

        pagination_html += '<button type="{t}" name="page" value="{val}" class="p-btn p-right-end {cl}"></button>'\
            .format(val=count_pages, cl=right_class, t=right_type)

        pagination_html += '</div></div>'

        return pagination_html
