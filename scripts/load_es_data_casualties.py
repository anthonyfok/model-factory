# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2020 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import json
import os
import sys

from elasticsearch import Elasticsearch
es = Elasticsearch()

if len(sys.argv) < 3:
    print('Usage: {} <path/to/data.geojson> <id-field>'.format(sys.argv[0]))
    sys.exit(1)

index_name = os.path.splitext(os.path.basename(sys.argv[1]))[0].lower()
id_field = sys.argv[2]

if es.indices.exists(index_name):
    es.indices.delete(index_name)

# index settings
settings = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0
    },
    "mappings": {
        "_meta": {
            "created_by": "load_es_data.py"
        },
        "properties": {
            "CensusPop": {
                "type": "long"
            },
            "Magnitude": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "Retrofit": {
            "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "Rupture_Name": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "Sauid": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "Source_Type": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "coordinates": {
                "type": "geo_shape"
            },
            "geom_point": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "sC_CasDay_crit": {
                "type": "long"
            },
            "sC_CasDay_min": {
                "type": "long"
            },
            "sC_CasDay_mod": {
                "type": "long"
            },
            "sC_CasDay_ser": {
                "type": "long"
            },
            "sC_CasNit_crit": {
                "type": "long"
            },
            "sC_CasNit_min": {
                "type": "long"
            },
            "sC_CasNit_mod": {
                "type": "long"
            },
            "sC_CasNit_ser": {
                "type": "long"
            },
            "sC_CasTrn_crit": {
                "type": "long"
            },
            "sC_CasTrn_min": {
                "type": "long"
            },
            "sC_CasTrn_mod": {
                "type": "long"
            },
            "sC_CasTrn_ser": {
                "type": "long"
            },
            "sL_Fatality": {
                "type": "long"
            }
        }
    }
}


# create index
es.indices.create(index=index_name, body=settings, request_timeout=90)

with open(sys.argv[1]) as fh:
    d = json.load(fh)

for f in d['features']:
    try:
        f['properties'][id_field] = int(f['properties'][id_field])
    except ValueError:
        f['properties'][id_field] = f['properties'][id_field]
    res = es.index(index=index_name, id=f['properties'][id_field], body=f)