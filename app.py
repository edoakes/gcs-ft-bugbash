import logging
from typing import Dict

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

import ray
from ray import serve

app = FastAPI()

logger = logging.getLogger("ray.serve")

@serve.deployment(num_replicas=2)
@serve.ingress(app)
class GetNodeID:
    @app.get("/")
    async def get_node_id(self) -> Dict[str, str]:
        node_id = str(ray.get_runtime_context().node_id.hex())
        logger.info(f"Node ID: {node_id}")
        return {"node_id": node_id}

app = GetNodeID.bind()
