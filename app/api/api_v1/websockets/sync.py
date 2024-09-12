import select
from typing import Annotated
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Query,
    Response,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from pydantic_core import to_json
from supabase import SupabaseAuthClient
from supabase_py_async import AsyncClient
from tomlkit import table

from app.api.database import init_super_client
from app.core.ws_manager import ConnectionManager
from app.schemas.item import ItemSync
from app.schemas.sync import ActionType, DescriptionType, SyncItemModel
from app.core.config import settings

router = APIRouter()


manager = ConnectionManager()

async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@router.websocket("/user/{user_id}/ws")
async def websocket_user_endpoint(
    *,
    websocket: WebSocket,
    user_id: str,
    token: str = Depends(get_cookie_or_token),
    super_client: AsyncClient = Depends(init_super_client),
):
    try:
        auth = await super_client.auth.get_user(token)
        if not auth:
            await websocket.send_denial_response(Response(status_code=403, content="Unauthorized"))
            return
    except Exception as e:
        await websocket.send_denial_response(Response(status_code=403, content="Unauthorized"))
        return

    await manager.connect(websocket)

    # await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            item: SyncItemModel = await SyncItemModel.from_json_text(data)
            super_client.postgrest.auth(token)
            # '{"images":[],"price":0.0,"quantity":0,"category":0,"barcode":"111111111111111","stock":0,"edited_at":"2024-09-06T09:21:18.080799","created_at":"2024-09-06T09:21:18.080845","user_id":"62bc4473-a284-4b72-8970-51f81fac223f","team_id":"00000000-0000-0000-0000-000000000000"}'
            # itemın id si yoksa supabase ekle
            # itemın id si varsa supabaseden aynı itemi kontrol et ve eşleşen itemi güncelle değiştirlme tarihi daha yeniyse güncelle

            will_send_sync_item = SyncItemModel(
                action=ActionType.UNKNOWN,
                item=item.item,
                type=item.type,
                is_synced=False,
                description=DescriptionType.UNKNOWN,
            )

            try:
                if item.type == "Item":
                    match item.action:
                        case ActionType.ADD:
                            if not item.item.id:
                                response = (
                                    await super_client.table("products")
                                    .insert(
                                        item.item.model_dump(
                                            exclude={"id", "dummy_id", "is_synced"}
                                        ),
                                        
                                    )
                                    .execute()
                                )

                                if response.data:
                                    will_send_sync_item.item = ItemSync(**response.data[0], is_synced=True,dummy_id=item.item.dummy_id)
                                    will_send_sync_item.action = ActionType.ADD
                                    will_send_sync_item.type = "Item"
                                    will_send_sync_item.is_synced = True
                                    will_send_sync_item.description = DescriptionType.SUCCESS
            
                            else:
                                data, count = (
                                    await super_client.table("items")
                                    .select("*")
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                _, got = data
                                if got:
                                    item_db = got[0]
                                    if item_db["updated_at"] < item.item.edited_at:
                                        response = (
                                            await super_client.table("items")
                                            .update(
                                                item.item.model_dump(
                                                    exclude={"dummy_id", "is_synced"}
                                                )
                                            )
                                            .eq("id", item.item.id)
                                            .execute()
                                        )
                                        if response.data:
                                            will_send_sync_item.item = ItemSync(**response["data"][0])
                                            will_send_sync_item.action = ActionType.UPDATE
                                            will_send_sync_item.type = "Item"
                                            will_send_sync_item.is_synced = True
                                            will_send_sync_item.description = DescriptionType.SUCCESS
                                    else:
                                        will_send_sync_item.item = ItemSync(**item_db)
                                        will_send_sync_item.action = ActionType.UNKNOWN
                                        will_send_sync_item.type = "Item"
                                        will_send_sync_item.is_synced = True  
                                        will_send_sync_item.description = DescriptionType.FETCH   


                        case ActionType.UPDATE:
                            if item.item.id:
                                data, count = (
                                    await super_client.table("items")
                                    .select("*")
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                _, got = data
                                if got:
                                    item_db = got[0]
                                    if item_db["updated_at"] < item.item.edited_at:
                                        response = (
                                            await super_client.table("items")
                                            .update(
                                                item.item.model_dump(
                                                    exclude={"dummy_id", "is_synced"}
                                                )
                                            )
                                            .eq("id", item.item.id)
                                            .execute()
                                        )

                                        if response.data:
                                            will_send_sync_item.item = ItemSync(**response["data"][0])
                                            will_send_sync_item.action = ActionType.UPDATE
                                            will_send_sync_item.type = "Item"
                                            will_send_sync_item.is_synced = True
                                            will_send_sync_item.description = DescriptionType.SUCCESS
                                    else:
                                        will_send_sync_item.item = ItemSync(**item_db)
                                        will_send_sync_item.action = ActionType.UNKNOWN
                                        will_send_sync_item.type = "Item"
                                        will_send_sync_item.is_synced = True
                                        will_send_sync_item.description = DescriptionType.FETCH
                            
                            else:
                                # item lokalde oluşturulup sonradan update gelmiş olabilir
                                # bu durumda itemın id si olmayacaktır
                                # bu durumda itemı ekleyeceğiz
                                response = (
                                    await super_client.table("items")
                                    .insert(
                                        item.item.model_dump(
                                            exclude={"id", "dummy_id", "is_synced"}
                                        )
                                    )
                                    .execute()
                                )

                                if response.data:
                                    will_send_sync_item.item = ItemSync(**response["data"][0])
                                    will_send_sync_item.action = ActionType.ADD
                                    will_send_sync_item.type = "Item"
                                    will_send_sync_item.is_synced = True
                                    will_send_sync_item.description = DescriptionType.SUCCESS

                        case ActionType.DELETE:
                            if item.item.id:
                                response = (
                                    await super_client.table("items")
                                    .delete()
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                will_send_sync_item.item = ItemSync(**response["data"][0])
                                will_send_sync_item.action = ActionType.DELETE
                                will_send_sync_item.type = "Item"
                                will_send_sync_item.is_synced = True
                                will_send_sync_item.description = DescriptionType.SUCCESS
                        case ActionType.UNKNOWN:
                            pass

                elif item.type == "Category":
                    match item.action:
                        case ActionType.ADD:
                            if not item.item.id:
                                response = (
                                    await super_client.table("categories")
                                    .insert(
                                        item.item.model_dump(
                                            exclude={"id", "dummy_id", "is_synced"}
                                        )
                                    )
                                    .execute()
                                )

                                if response.data:
                                    will_send_sync_item.item = ItemSync(**response["data"][0])
                                    will_send_sync_item.action = ActionType.ADD
                                    will_send_sync_item.type = "Category"
                                    will_send_sync_item.is_synced = True
                                    will_send_sync_item.description = DescriptionType.SUCCESS

                            else:
                                data, count = (
                                    await super_client.table("categories")
                                    .select("*")
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                _, got = data
                                if got:
                                    item_db = got[0]
                                    if item_db["updated_at"] < item.item.edited_at:
                                        response = (
                                            await super_client.table("categories")
                                            .update(
                                                item.item.model_dump(
                                                    exclude={"dummy_id", "is_synced"}
                                                )
                                            )
                                            .eq("id", item.item.id)
                                            .execute()
                                        )

                                        if response.data:
                                            will_send_sync_item.item = ItemSync(**response["data"][0])
                                            will_send_sync_item.action = ActionType.UPDATE
                                            will_send_sync_item.type = "Category"
                                            will_send_sync_item.is_synced = True
                                            will_send_sync_item.description = DescriptionType.SUCCESS

                                    else:
                                        will_send_sync_item.item = ItemSync(**item_db)
                                        will_send_sync_item.action = ActionType.UNKNOWN
                                        will_send_sync_item.type = "Category"
                                        will_send_sync_item.is_synced = True
                                        will_send_sync_item.description = DescriptionType.FETCH

                        case ActionType.UPDATE:
                            if item.item.id:
                                data, count = (
                                    await super_client.table("categories")
                                    .select("*")
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                _, got = data
                                if got:
                                    item_db = got[0]
                                    if item_db["updated_at"] < item.item.edited_at:
                                        response = (
                                            await super_client.table("categories")
                                            .update(
                                                item.item.model_dump(
                                                    exclude={"dummy_id", "is_synced"}
                                                )
                                            )
                                            .eq("id", item.item.id)
                                            .execute()
                                        )

                                        if response.data:
                                            will_send_sync_item.item = ItemSync(**response["data"][0])
                                            will_send_sync_item.action = ActionType.UPDATE
                                            will_send_sync_item.type = "Category"
                                            will_send_sync_item.is_synced = True
                                            will_send_sync_item.description = DescriptionType.SUCCESS
                                    else:
                                        will_send_sync_item.item = ItemSync(**item_db)
                                        will_send_sync_item.action = ActionType.UNKNOWN
                                        will_send_sync_item.type = "Category"
                                        will_send_sync_item.is_synced = True
                                        will_send_sync_item.description = DescriptionType.FETCH
                            
                            else:
                                # item lokalde oluşturulup sonradan update gelmiş olabilir
                                # bu durumda itemın id si olmayacaktır
                                # bu durumda itemı ekleyeceğiz
                                response = (
                                    await super_client.table("categories")
                                    .insert(
                                        item.item.model_dump(
                                            exclude={"id", "dummy_id", "is_synced"}
                                        )
                                    )
                                    .execute()
                                )

                                if response.data:
                                    will_send_sync_item.item = ItemSync(**response["data"][0])
                                    will_send_sync_item.action = ActionType.ADD
                                    will_send_sync_item.type = "Category"
                                    will_send_sync_item.is_synced = True
                                    will_send_sync_item.description = DescriptionType.SUCCESS

                        case ActionType.DELETE:
                            if item.item.id:
                                response = (
                                    await super_client.table("categories")
                                    .delete()
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                will_send_sync_item.item = ItemSync(**response["data"][0])
                                will_send_sync_item.action = ActionType.DELETE
                                will_send_sync_item.type = "Category"
                                will_send_sync_item.is_synced = True
                                will_send_sync_item.description = DescriptionType.SUCCESS

                        case ActionType.UNKNOWN:
                            will_send_sync_item.item = item.item
                            will_send_sync_item.action = item.action
                            will_send_sync_item.is_synced = False
                            will_send_sync_item.description = DescriptionType.UNKNOWN

        
            except Exception as e:
                will_send_sync_item.item = item.item
                will_send_sync_item.action = item.action
                will_send_sync_item.is_synced = False
                will_send_sync_item.description = DescriptionType.FAILURE

            finally:
                await manager.send_personal_message( will_send_sync_item.model_dump_json(),websocket=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} left the chat")
    
    # except WebSocketException as e:
    #     manager.disconnect(websocket)
    #     # await websocket.close(code=e.code)

@router.websocket("/team/{team_id}/ws")
async def websocket_team_endpoint(
    websocket: WebSocket,
    team_id: str,
    token: str = Depends(get_cookie_or_token),
    super_client: AsyncClient = Depends(init_super_client),
):
    try:
        auth = await super_client.auth.get_user(token)
        if not auth:
            await websocket.send_denial_response(Response(status_code=403, content="Unauthorized"))
            return
        
        # kullanıcı teamde mi kontrol et
        data, count = (
            await super_client.table("teams_user")
            .select("*")
            .eq("user_id", auth.user.id)
            .eq("team_id", team_id)
            .execute()
        )

        if count == 0:
            await websocket.send_denial_response(Response(status_code=403, content="Unauthorized"))
            return

    except Exception as e:
        await websocket.send_denial_response(Response(status_code=403, content="Unauthorized"))
        return

    await manager.connect(websocket)

    # await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            item: SyncItemModel = await SyncItemModel.from_json_text(data)
            super_client.postgrest.auth(token)
            # '{"images":[],"price":0.0,"quantity":0,"category":0,"barcode":"111111111111111","stock":0,"edited_at":"2024-09-06T09:21:18.080799","created_at":"2024-09-06T09:21:18.080845","user_id":"62bc4473-a284-4b72-8970-51f81fac223f","team_id":"00000000-0000-0000-0000-000000000000"}'
            # itemın id si yoksa supabase ekle
            # itemın id si varsa supabaseden aynı itemi kontrol et ve eşleşen itemi güncelle değiştirlme tarihi daha yeniyse güncelle

            will_send_sync_item = SyncItemModel(
                action=ActionType.UNKNOWN,
                item=item.item,
                type=item.type,
                is_synced=False,
                description=DescriptionType.UNKNOWN,
            )

            try:
                if item.type == "Item":
                    match item.action:
                        case ActionType.ADD:
                            if not item.item.id:
                                response = (
                                    await super_client.table("products")
                                    .insert(
                                        item.item.model_dump(
                                            exclude={"id", "dummy_id", "is_synced"}
                                        ),
                                        
                                    )
                                    .execute()
                                )

                                if response.data:
                                    will_send_sync_item.item = ItemSync(**response.data[0], is_synced=True,dummy_id=item.item.dummy_id)
                                    will_send_sync_item.action = ActionType.ADD
                                    will_send_sync_item.type = "Item"
                                    will_send_sync_item.is_synced = True
                                    will_send_sync_item.description = DescriptionType.SUCCESS
            
                            else:
                                data, count = (
                                    await super_client.table("items") 
                                    .select("*")
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                _, got = data
                                if got:
                                    item_db = got[0]
                                    if item_db["updated_at"] < item.item.edited_at:
                                        response = (
                                            await super_client.table("items")
                                            .update(
                                                item.item.model_dump(
                                                    exclude={"dummy_id", "is_synced"}
                                                )
                                            )
                                            .eq("id", item.item.id)
                                            .execute()
                                        )
                                        if response.data:
                                            will_send_sync_item.item = ItemSync(**response["data"][0])
                                            will_send_sync_item.action = ActionType.UPDATE
                                            will_send_sync_item.type = "Item"
                                            will_send_sync_item.is_synced = True
                                            will_send_sync_item.description = DescriptionType.SUCCESS
                                    else:
                                        will_send_sync_item.item = ItemSync(**item_db)
                                        will_send_sync_item.action = ActionType.UNKNOWN
                                        will_send_sync_item.type = "Item"
                                        will_send_sync_item.is_synced = True  
                                        will_send_sync_item.description = DescriptionType.FETCH
                        case ActionType.UPDATE:
                            if item.item.id:
                                data, count = (
                                    await super_client.table("items")
                                    .select("*")
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                _, got = data
                                if got:
                                    item_db = got[0]
                                    if item_db["updated_at"] < item.item.edited_at:
                                        response = (
                                            await super_client.table("items")
                                            .update(
                                                item.item.model_dump(
                                                    exclude={"dummy_id", "is_synced"}
                                                )
                                            )
                                            .eq("id", item.item.id)
                                            .execute()
                                        )

                                        if response.data:
                                            will_send_sync_item.item = ItemSync(**response["data"][0])
                                            will_send_sync_item.action = ActionType.UPDATE
                                            will_send_sync_item.type = "Item"
                                            will_send_sync_item.is_synced = True
                                            will_send_sync_item.description = DescriptionType.SUCCESS
                                    else:
                                        will_send_sync_item.item = ItemSync(**item_db)
                                        will_send_sync_item.action = ActionType.UNKNOWN
                                        will_send_sync_item.type = "Item"
                                        will_send_sync_item.is_synced = True
                                        will_send_sync_item.description = DescriptionType.FETCH
                            
                            else:
                                # item lokalde oluşturulup sonradan update gelmiş olabilir
                                # bu durumda itemın id si olmayacaktır
                                # bu durumda itemı ekleyeceğiz
                                response = (
                                    await super_client.table("items")
                                    .insert(
                                        item.item.model_dump(
                                            exclude={"id", "dummy_id", "is_synced"}
                                        )
                                    )
                                    .execute()
                                )

                                if response.data:
                                    will_send_sync_item.item = ItemSync(**response["data"][0])
                                    will_send_sync_item.action = ActionType.ADD
                                    will_send_sync_item.type = "Item"
                                    will_send_sync_item.is_synced = True
                                    will_send_sync_item.description = DescriptionType.SUCCESS

                        case ActionType.DELETE:
                            if item.item.id:
                                response = (
                                    await super_client.table("items")
                                    .delete()
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                will_send_sync_item.item = ItemSync(**response["data"][0])
                                will_send_sync_item.action = ActionType.DELETE
                                will_send_sync_item.type = "Item"
                                will_send_sync_item.is_synced = True
                                will_send_sync_item.description = DescriptionType.SUCCESS
                        case ActionType.UNKNOWN:
                            pass
                            
                elif item.type == "Category":
                    match item.action:
                        case ActionType.ADD:
                            if not item.item.id:
                                response = (
                                    await super_client.table("categories")
                                    .insert(
                                        item.item.model_dump(
                                            exclude={"id", "dummy_id", "is_synced"}
                                        )
                                    )
                                    .execute()
                                )

                                if response.data:
                                    will_send_sync_item.item = ItemSync(**response["data"][0])
                                    will_send_sync_item.action = ActionType.ADD
                                    will_send_sync_item.type = "Category"
                                    will_send_sync_item.is_synced = True
                                    will_send_sync_item.description = DescriptionType.SUCCESS

                            else:
                                data, count = (
                                    await super_client.table("categories")
                                    .select("*")
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                _, got = data
                                if got:
                                    item_db = got[0]
                                    if item_db["updated_at"] < item.item.edited_at:
                                        response = (
                                            await super_client.table("categories")
                                            .update(
                                                item.item.model_dump(
                                                    exclude={"dummy_id", "is_synced"}
                                                )
                                            )
                                            .eq("id", item.item.id)
                                            .execute()
                                        )

                                        if response.data:
                                            will_send_sync_item.item = ItemSync(**response["data"][0])
                                            will_send_sync_item.action = ActionType.UPDATE
                                            will_send_sync_item.type = "Category"
                                            will_send_sync_item.is_synced = True
                                            will_send_sync_item.description = DescriptionType.SUCCESS

                                    else:
                                        will_send_sync_item.item = ItemSync(**item_db)
                                        will_send_sync_item.action = ActionType.UNKNOWN
                                        will_send_sync_item.type = "Category"
                                        will_send_sync_item.is_synced = True
                                        will_send_sync_item.description = DescriptionType.FETCH

                        case ActionType.UPDATE:
                            if item.item.id:
                                data, count = (
                                    await super_client.table("categories")
                                    .select("*")
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                _, got = data
                                if got:
                                    item_db = got[0]
                                    if item_db["updated_at"] < item.item.edited_at:
                                        response = (
                                            await super_client.table("categories")
                                            .update(
                                                item.item.model_dump(
                                                    exclude={"dummy_id", "is_synced"}
                                                )
                                            )
                                            .eq("id", item.item.id)
                                            .execute()
                                        )

                                        if response.data:
                                            will_send_sync_item.item = ItemSync(**response["data"][0])
                                            will_send_sync_item.action = ActionType.UPDATE
                                            will_send_sync_item.type = "Category"
                                            will_send_sync_item.is_synced = True
                                            will_send_sync_item.description = DescriptionType.SUCCESS
                                    else:
                                        will_send_sync_item.item = ItemSync(**item_db)
                                        will_send_sync_item.action = ActionType.UNKNOWN
                                        will_send_sync_item.type = "Category"
                                        will_send_sync_item.is_synced = True
                                        will_send_sync_item.description = DescriptionType.FETCH

                            else:
                                # item lokalde oluşturulup sonradan update gelmiş olabilir
                                # bu durumda itemın id si olmayacaktır
                                # bu durumda itemı ekleyeceğiz
                                response = (
                                    await super_client.table("categories")
                                    .insert(
                                        item.item.model_dump(
                                            exclude={"id", "dummy_id", "is_synced"}
                                        )
                                    )
                                    .execute()
                                )

                                if response.data:
                                    will_send_sync_item.item = ItemSync(**response["data"][0])
                                    will_send_sync_item.action = ActionType.ADD
                                    will_send_sync_item.type = "Category"
                                    will_send_sync_item.is_synced = True
                                    will_send_sync_item.description = DescriptionType.SUCCESS

                        case ActionType.DELETE:
                            if item.item.id:
                                response = (
                                    await super_client.table("categories")
                                    .delete()
                                    .eq("id", item.item.id)
                                    .execute()
                                )
                                will_send_sync_item.item = ItemSync(**response["data"][0])
                                will_send_sync_item.action = ActionType.DELETE
                                will_send_sync_item.type = "Category"
                                will_send_sync_item.is_synced = True
                                will_send_sync_item.description = DescriptionType.SUCCESS

                        case ActionType.UNKNOWN:
                            will_send_sync_item.item = item.item
                            will_send_sync_item.action = item.action
                            will_send_sync_item.is_synced = False
                            will_send_sync_item.description = DescriptionType.UNKNOWN


            except Exception as e:
                will_send_sync_item.item = item.item
                will_send_sync_item.action = item.action
                will_send_sync_item.is_synced = False
                will_send_sync_item.description = DescriptionType.FAILURE

            finally:
                await manager.send_personal_message( will_send_sync_item.model_dump_json(),websocket=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{team_id} left the chat")
