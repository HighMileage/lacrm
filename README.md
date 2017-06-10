# lacrm
![](https://travis-ci.org/HighMileage/lacrm.svg?branch=master)
An intuitive [Less Annoying CRM](https://www.lessannoyingcrm.com) REST API client written in Python.

## Installation and Configuration
```
pip install lacrm
```

`lacrm` will attempt to look for a `.lacrm` file in your home directory. This file should have your LACRM `user_code` and `api_token` separated by a colon:
```
#USER_CODE:API_TOKEN
ABC12:ASDLFKJP0R3UP0Q32U0P91283JFIOWUERV
```

## Usage
If you've configured a dot file in your home directory:
```python
>>> from lacrm import Lacrm
>>> lacrm = Lacrm()
```

Otherwise:
```python
>>> from lacrm import Lacrm
>>> lacrm = Lacrm(user_code='ABC12', api_token='ASDLFKJP0R3UP0Q32U0P91283JFIOWUERV')
>>> data = {'FirstName': 'Mark', 'LastName': 'Wrighton'}
>>> lacrm.create_contact(data)
>>> '123940'
```

Sometimes you might want to interact with the raw LACRM response yourself. In that case you can pass the `raw_response` flag as `True`
```python
>>> lacrm.edit_contact('123940',{'FirstName': 'Trent', 'LastName':'Reznor'}, raw_response=True)
>>> {u'Success': True}
```

## Documentation
Full documentation coming soon.
