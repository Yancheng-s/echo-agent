from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from services.auth import get_current_user
from database import get_db

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/research")
async def research_ws(websocket: WebSocket):
    await websocket.accept()

    # TODO: 验证 token，后续 Phase 实现
    # token = websocket.query_params.get("token")
    # user = get_current_user(token)

    try:
        while True:
            data = await websocket.receive_json()
            query = data.get("query", "")

            # TODO: 接入 Echo Pipeline，后续 Phase 实现
            await websocket.send_json({"type": "status", "message": f"开始研究: {query}"})

    except WebSocketDisconnect:
        pass
