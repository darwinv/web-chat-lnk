"""
A simple tool for converting JSON to an HTML table.
This is based off of the `json2html` project.
Their code can be found at https://github.com/softvar/json2html

#Aca va ejemplos de como se debe armar json
Columnas personalizadas # Aca va explicacion y ejemplo de las columas personalizadas
'concat':
'detail':
'delete':
'link':
"""
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

def convert(data, table_attributes=None,header=None,custom_column=None,actual_page=None,attributes_colum=None):
    
    generateTableObj    = generateTableList(table_attributes=table_attributes)  #  Se inicia la clase y definen atributos de la tabla
    
    if type(data) is dict and 'results' in data:  # Si la data no tiene el elemento "results" se setea "None" para eliminar errores de compilacion
        dataTable = data['results']
    else:
        dataTable = None
        
    html_output         = generateTableObj.convert(dataTable,header=header,custom_column=custom_column,attributes_colum=attributes_colum)  # Construye el cuerpo hasta el cierre de la etiqueta </table>

    if actual_page is not None and type(data) is dict and 'total_pages' in data:  # Si se envia la cantidad de paginas para el listado
        html_output    += generateTableObj.pagination(count_pages=data['total_pages'], actual_page=actual_page);

    return html_output

def getActualPage(request):
    if 'page' in request.GET:
        actual_page = request.GET['page']
    else:
        actual_page = 1
    return actual_page
    
class generateTableList(object):

    """
    Class that manages the conversion of a JSON object to a string of HTML.

    Methods
    -------
    convert(json_input)
        Converts JSON to HTML.
    """

    def __init__(self, table_attributes=None):
        table_attributes_defaul = {"class": "table table-striped table-bordered table-hover "}        
        
        
        if table_attributes is not None and not isinstance(table_attributes, dict):
            raise TypeError("Table attributes must be either a `dict` or `None`.")
        if table_attributes:
            table_attributes_defaul = self.mergeAtributes(default=table_attributes_defaul,custom=table_attributes)

        self._table_opening_tag = "<table{:s}>".format(generateTableList._dict_to_html_attributes(table_attributes_defaul))


    def convert(self, json_input,header,custom_column=None,attributes_colum=None):
        """
        Converts JSON to HTML Table format.

        Parameters
        ----------
        json_input : dict
            JSON object to convert into HTML.

        Returns
        -------
        str
            String of converted HTML.
        """
        
        html_output = "<div class='overflow-auto'>"
        html_output += self._table_opening_tag
        html_output += self._markup_header_row(header.keys())

        if json_input:
            html_output += "<tr>"
            for listData in json_input:
                for key in header.values():

                    if key in custom_column:                    
                        customValue = self.create_custom_value(listData,custom_column[key])                        
                        value = customValue
                    elif key in listData.keys() and listData[key]:
                        value = listData[key]
                    else:
                        value = ""

                    html_output += self.create_table_data(key,value,attributes_colum)

                html_output += "</tr>"
        else:
            html_output += "<tr><td colspan='{}'>{}</td></tr>".format(len(header.keys()),_("search is empty").title())
        html_output += "</table></div>"
        return html_output

    def create_table_data(self,key,value,attributes_colum):
        attrs = ""
        if type(attributes_colum) is dict and key in attributes_colum:
            for attr_name in attributes_colum[key]:
                attrs += "{}='{}'".format(attr_name,attributes_colum[key][attr_name])


        return "<td {attrs}>{value}</td>".format(value=value,attrs=attrs)

    def create_custom_value(self, row_data,custom_column_data):
        value = ""
        type_colum = custom_column_data['type']
        data    = custom_column_data['data']

        if type_colum == 'concat':
            texts = []
            separator = ""  # Separador entre los String concatenados
            if 'separator' in custom_column_data:
                separator = custom_column_data['separator']


            for key_column in data:

                if key_column in row_data:  # Si la columna existe en la data enviada
                    if type(data) is dict:  # Si la data es un dict, recorremos recursivamente den elemento padre
                        custom_column_data_aux = {'type':type_colum,'data':data[key_column],'separator':separator}
                        recursion = self.create_custom_value(row_data[key_column],custom_column_data_aux)
                        texts.append(str(recursion))
                    else:
                        texts.append(str(row_data[key_column]))

                elif type(key_column) is str:  # Si el valor es un simple string, se guarda
                    texts.append(str(key_column))


            value = separator.join( texts )  # Se crea un solo string de la lista, separadas por el separador definido


        if type_colum == 'detail':
            #  Columna estandar para mostrar icono de ir al detalle
            value  +='<a href="{}"><i class="fa fa-search"></i></a>'.format(reverse(data['url'], args=(row_data[data['key']],)))

        if type_colum == 'delete':
            #  Columna estandar para mostrar icono de borrar
            value  +='<i class="fa fa-trash pointer color-red ico-delete-row" data-url="{}" data-id="{id}"></i>'.format(reverse(data['url']),id=row_data[data['key']])

        if type_colum == 'link':
            """"
            Caso para crear links personalizados, con parametros y argumentos
            
            Requerido: data['text'], data['url']
            data['text']: Define el texto a mostrar en el listadao
            data['url']: nombre de la url
            data['arguments']: define argumentos tipo get e.g. ?client=69            
            data['key']: define valor a pasar en la funcion reverse

            """
            arguments = url = ''

            if 'arguments' in data:
                arguments += '?'
                data_arg = data['arguments']
                for arg_key in data_arg:
                    argument_value = ''
                    if data_arg[arg_key] in row_data:
                        argument_value = row_data[data_arg[arg_key]]
                    else:
                        argument_value = data_arg[arg_key]
                    arguments += '{param}={value}'.format(param=arg_key, value=argument_value)

            if 'key' in data:
                url = reverse(data['url'],args=(row_data[data['key']],))
            else:
                url = reverse(data['url'])

            value  +='<a href="{url}{arg}">{text}</i></a>'.format(url=url, arg=arguments, text=data['text'])

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
        html_output = "<tr>"
        for key in headers:
            html_output += "<th>{}</th>".format(self.capitalize(key))
        return html_output + "</tr>"


    @staticmethod
    def capitalize(line):
        return line[0].upper() + line[1:]
        #return ' '.join(s[0].upper() + s[1:] for s in line.split(' '))
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

    



    def mergeAtributes(self, default,custom):
        if 'class' in custom:
            default['class'] += custom['class']

        return dict(custom, **default);


    def pagination(self,count_pages,actual_page):
        left_class  = right_class   = ''
        leftType    = rightType     = 'submit'
        page        = int(actual_page)

        paginationHTML  = '<div class="aling-right"><div class="pagination">'
        if page<=1:
            left_class   = 'disable'
            leftType    = 'button'

        paginationHTML += '<button type="{t}" name="page" value="1" class="p-btn p-left-start {}"></button>'.format(left_class,t=leftType)

        paginationHTML += '<button type="{t}" name="page" value="{}" class="p-btn p-left {}"></button>'.format(int(page)-1,left_class,t=leftType)
        
        paginationHTML += '<spam>{p} {} {of} {}</spam>'.format(page,count_pages,p=_('page').title(),of=_('of'))
        
        if page>=count_pages:
            right_class  = 'disable'
            rightType   = 'button'
        paginationHTML += '<button type="{t}" name="page" value="{}" class="p-btn p-right {}"></button>'.format(int(page)+1,right_class,t=rightType)

        paginationHTML += '<button type="{t}" name="page" value="{}" class="p-btn p-right-end {}"></button>'.format(count_pages,right_class,t=rightType)

        paginationHTML += '</div></div>'

        return paginationHTML
