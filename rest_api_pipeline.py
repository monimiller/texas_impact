from typing import Any, Optional

import dlt
from dlt.common.pendulum import pendulum
from dlt.sources.rest_api import (
    RESTAPIConfig,
    check_connection,
    rest_api_resources,
    rest_api_source,
)


"""
https://api.legiscan.com/?key=APIKEY&op=getSearch&state=STATE&query=QUERY
"""
def load_legiscan() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_legiscan",
        destination='duckdb',
        dataset_name="rest_api_data",
    )

    legiscan_source = rest_api_source(
        {
            "client": {
                "base_url": "https://api.legiscan.com/",
                # If you leave out the paginator, it will be inferred from the API:
                # "paginator": "json_link",
            },
            "resource_defaults": {
                "endpoint": {
                    "params": {
                        "key": api_key,
                        "op": "getSearch",
                        # Actual params
                        "state": "TX",
                        "query": "Feminine Hygiene",
                        # year (Optional) Year where 1=all, 2=current, 3=recent, 4=prior, >1900=exact [Default: 2]
                        # page (Optional) Result set page number to return [Default: 1]
                    },
                },
            },
            # "resources": [
            #     "searchresult",
            #     "summary",
            #     "results",
            # ],
        }
    )

    def check_network_and_authentication() -> None:
        (can_connect, error_msg) = check_connection(
            legiscan_source,
            "not_existing_endpoint",
        )
        if not can_connect:
            pass  # do something with the error message

    check_network_and_authentication()

    load_info = pipeline.run(legiscan_source)
    print(load_info)  # noqa: T201


if __name__ == "__main__":
    load_legiscan()
