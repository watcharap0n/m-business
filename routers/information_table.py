from fastapi import APIRouter

router = APIRouter()

data = [
    {
        'tag': 'a',
        'name': 'watcharapon',
        'product': 'consultant',
        'tel': '0656791794',
        'email': 'aasd@gmail.com'
    },
    {
        'tag': 'b',
        'name': 'thiphaporn',
        'product': 'pusit',
        'tel': '0632414155',
        'email': 'wertt@gmail.com'
    },
    {
        'tag': 'a',
        'name': 'mawin',
        'product': 'realestate',
        'tel': '0512414552',
        'email': 'erakei@gmail.com'
    }
]


@router.get('/table')
def info_table_get():
    return data


@router.post('/table')
def info_table_post():
    pass


@router.put('/table')
def info_table_put():
    pass


@router.delete('/table')
def info_table_delete():
    pass
