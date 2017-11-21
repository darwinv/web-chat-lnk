
from django.utils.translation import ugettext_lazy as _
        
class ChoicesAPI:
    """
        Clase Choices para manejo de opciones en los modelos
        cada atributo de la clase es una opcion de modelo
        la estructura en los nombres de los choises es la siguiente
        nombre del modelo + piso + nombre de atributo
        e.g: "client_type_client" o "client_sex" 
    """

    # User Model
    user_document_type = (
        ('0',_('DNI')),
        ('1',_('Passport')),
        ('2',_('Foreign Card')),
    )

    # Client Model
    client_type_client = (
        ('n',_('Natural')),
        ('b',_('Bussiness')),
    )

    client_sex = (
        ('n',_('Male')),
        ('b',_('Female')),
    )
    client_civil_state = (
        ('c',_('cohabiting')),
        ('e',_('separated')),
        ('m',_('married')),
        ('w',_('widower')),
        ('d',_('divorced')),
        ('s',_('single')),
    )

    client_ocupation = (
        ('0',_('Employer')),
        ('1',_('Independent worker')),
        ('2',_('Employee')),
        ('3',_('Worker')),
        ('4',_('Worker in a family business')),
        ('5',_('Home worker')),
        ('6',_('Other')),
    )

    # Specialist Model
    specialist_type_specialist = (
        ('m',_('Main')),
        ('a',_('Associate')),
    )

    # Specialistcontract Model
    specialistcontract_state = (
        ('r',_('Requested')),
        ('a',_('Accepted')),
        ('d',_('Declined')),
    )

    # Promotion Model
    promotions_type = (
        ('p',_('Percentage')),
        ('n',_('Number')),
    )


    # Purchase Model
    purchase_status = (
        ('0',_('Pending')),
        ('1',_('Paid')),
    )

    # Purchase Model
    fee_status = (
        ('1',_('Pending')),
        ('2',_('Paid')),
    )

    # CulqiPayment Model
    culqipayment_status = (
        ('w',_('Wait')),
        ('d',_('Denied')),
        ('e',_('Exhaled')),
        ('p',_('Paid')),
    )

    # Query Model
    query_status = (
        ('0',_('Requested')), # Preguntada, pendiente de derivar o responder
        ('1',_('Requested Derived')), # derivada, pendiente de declinar o responder, reconsulta
        ('2',_('Pending Response')), # derivada a asociado, pendiente de respuesta
        ('3',_('Pending Main Response')), # principal, pendiente de respuesta
        ('4',_('Answered Main')), # respondida por principal
        ('5',_('Answered')), # respondida por asociado
        ('6',_('Absolved Main')), # resuelta por principal
        ('7',_('Absolved')), # resuelta por asociado
    )


    # Message Model
    message_msg_type = (
        ('q',_('query')), # es de tipo consulta
        ('r',_('requery')), # es de tipo reconsulta
        ('a',_('answer')), # es de tipo respuesta
    )

    # MessageFile Model
    messagefile_type_file = (
        ('0',_('Image')),
        ('1',_('Voice')),
        ('2',_('Document')),
    )

    # AlertCategory Model
    alertcategory_name = (
        ('c',_('Critic')),
        ('m',_('Moderate')),
        ('p',_('Positive')),
    )

