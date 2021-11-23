# mieagro-be

MIE AGRO Middleware application for Odoo and SAP

to download **POS Order** record, use **CURL** command line below:

```js
curl -o pos-order-2021-11-13.csv 'http://localhost/api/v1/download'
```

History record download:

```js
curl -o pos-order-2021-11-13.csv 'http://localhost/api/v1/download?to_date=2021-11-13'
```
