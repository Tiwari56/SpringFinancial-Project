{
    "name" : 'CRM fields Customization',
    'summery':'Custome CRM customization with custome api etc.',
    'category':'TEST',
    'author':'Nishit Tiwari',
    "version":  "1.0.0",
    'sequence':1,
    'depends' :['web','crm'] , 
    'data'  :[
        'security/ir.model.access.csv',
        'views/crm.xml',
        'data/stage_data.xml',
            ],
    'application' :True,
    "assets": {
        'web.assets_backend': [
            "crm_field_customization/static/src/**/*",
        ]
    }
}

