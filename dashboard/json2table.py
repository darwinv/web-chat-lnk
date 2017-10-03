"""
A simple tool for converting JSON to an HTML table.
This is based off of the `json2html` project.
Their code can be found at https://github.com/softvar/json2html
"""
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

def convert(data, table_attributes=None,header=None,custom_column=None,actual_page=None):

    generateTableObj    = generateTableList(table_attributes=table_attributes)
    
    if type(data) is dict and 'list' in data:
        dataTable = data['list']
    else:
        dataTable = None
        
    html_output         = generateTableObj.convert(dataTable,header=header,custom_column=custom_column)

    if actual_page is not None and type(data) is dict and 'countPages' in data:
        html_output        += generateTableObj.pagination(count_pages=data['countPages'], actual_page=actual_page);
    return html_output

def getActualPage(request):
    if 'page' in request.GET:
        actual_page = request.GET['page']
    elif 'actual_page' in request.GET:
        actual_page = request.GET['a_page']
    else:
        actual_page = 0
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


    def convert(self, json_input,header,custom_column=None):
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
                        customValue = self.create_custom_column(listData,key,custom_column[key])
                        html_output += "<td>{}</td>".format(customValue)
                    elif key in listData.keys():
                        html_output += "<td>{}</td>".format(listData[key])
                    else:
                        html_output += "<td></td>"
                html_output += "</tr>"
        else:
            html_output += "<tr><td colspan='{}'>{}</td></tr>".format(len(header.keys()),_("search is empty").title())
        html_output += "</table></div>"
        return html_output


    def create_custom_column(self, list,key,custom_column_data):
        value = ""

        if custom_column_data['type'] == 'concat':            
            for key in custom_column_data['data']:
                value+=" {}".format(list[key])

        if custom_column_data['type'] == 'detail':
            data    = custom_column_data['data']
            value  +='<a href="'+reverse(data['href'], args=(list[data['key']],))+'"><i class="fa fa-search"></i></a>'

        if custom_column_data['type'] == 'delete':
            data    = custom_column_data['data']
            value  +='<i class="fa fa-trash pointer {} color-red" data-id="{id}"></i>'.format(data['class'],id=list[data['key']])

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
        left_class  = right_class    = ''
        leftType    = rightType     = 'submit'
        page        = int(actual_page)

        paginationHTML  = '<div class="aling-right"><div class="pagination">'
        if page<=1:
            left_class   = 'disable'
            leftType    = 'button'
        paginationHTML += '<button type="{t}" name="page" value="{}" class="p-btn p-left {}"></button>'.format(int(page)-1,left_class,t=leftType)
        
        paginationHTML += '<spam>{p} {} {of} {}</spam>'.format(page,count_pages,p=_('page').title(),of=_('of'))
        
        if page>=count_pages:
            right_class  = 'disable'
            rightType   = 'button'
        paginationHTML += '<button type="{t}" name="page" value="{}" class="p-btn p-right {}"></button>'.format(int(page)+1,right_class,t=rightType)


        paginationHTML += '</div></div>'
        paginationHTML += '<input type="hidden" name="a_page" value="{}">'.format(page)

        return paginationHTML
