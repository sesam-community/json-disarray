[![Build Status](https://travis-ci.org/sesam-community/mdmx.svg?branch=master)](https://travis-ci.org/sesam-community/mdmx)
Sesam.io sink to MDMx

This MS convert array of element(s) [{}] into a single element {} as required by the MDMx api.

Example System Config

```json
{
  "_id": "mdmx",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "BASE_URL": "https://some.url/api",
      "CLIENT-ID": "$ENV(mdmx-client-id)",
      "CLIENT-SECRET": "$SECRET(mdmx-client-secret)",
      "GRANT_TYPE": "client_credentials",
      "TOKEN_URL": "https://generic.ouath-provider/connect/token"
    },
    "image": "sesamcommunity/json-disarray:1.1.1",
    "port": 5000
  },
  "verify_ssl": true
}
```

Example endpoint pipe config

```json
{
  "_id": "meterpoint-mdmx-endpoint",
  "type": "pipe",
  "source": {
    "type": "dataset",
    "dataset": "meterpoint-mdmx"
  },
  "sink": {
    "type": "json",
    "system": "mdmx",
    "url": "/meteringpoints"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["filter",
          ["not", "_S._deleted"]
        ],
        ["copy", "*", "_*"]
      ]
    }
  },
  "batch_size": 1,
  "remove_namespaces": true
}
```
