import logging
from elasticlogs.parameter_sources.randomevent import RandomEvent

logger = logging.getLogger("track.elasticlogs")

class ElasticlogsBulkSource:
    def __init__(self, indices, params):
        self._indices = indices
        self._params = params
        self._randomevent = RandomEvent(params)

        self._bulk_size = 1000
        if 'bulk-size' in params.keys():
            self._bulk_size = params['bulk-size']

        self._default_index = False
        if 'index' not in params.keys():
            if len(indices) > 1:
                logger.info("[bulk] More than one index specified in track configuration. Will use the first one ({})".format(indices[0]['name']))
            else:
                logger.info("[bulk] Using index specified in track configuration ({})".format(indices[0]['name']))

            self._params['index'] = indices[0]['name']
            self._default_index = True

        else:
            logger.info("[bulk] Index pattern specified in parameters ({}) will be used".format(params['index']))

        if 'type' not in params.keys():
            self._params['type'] = indices[0]['types'][0]['name']

    def partition(self, partition_index, total_partitions):
        return self

    def size(self):
        return 1

    def params(self):
        # Build bulk array
        bulk_array = []
        for x in range(0, self._bulk_size):
            evt, idx, typ = self._randomevent(self._params)
            bulk_array.append({'index': {'_index': idx, '_type': typ}})
            bulk_array.append(evt)

        response = { "body": bulk_array, "action_metadata_present": True }

        if "pipeline" in params.keys():
            response["pipeline"] = params["pipeline"]

        return response
