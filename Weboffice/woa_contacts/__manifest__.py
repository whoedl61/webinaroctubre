# -*- coding: utf-8 -*-
{
    'name' : 'WOA Contacts',

    'version' : '',
    'summary': 'Contacts',
    'sequence': 15,
    'description': """
    """,
    'category': '',
    'website': 'https://www.weboffice.at',

    'images' : [],
    'depends' : ['base', 'sale'],

    'data': [

        # Security
        'security/ir.model.access.csv',

        # Data

        # Views
        'views/inherits/res_partner_views.xml',
        'views/inherits/sale_views.xml',
        'views/inherits/crm_phonecall.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_auto_install_l10n',
}
