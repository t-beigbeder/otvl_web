import logging
import copy
import os

from fastapi import FastAPI, HTTPException, Query, status, Request, Depends
from fastapi.responses import JSONResponse, FileResponse
from starlette.middleware.cors import CORSMiddleware

from otvl_web import context
from otvl_web.content import ContentFetcher
from otvl_web.html4bots import HtmlFetcher
from otvl_web.index import IndexFetcher
from otvl_web.sitemap import SiteMapFetcher


_ctx = context.Context()


def get_ctx():
    return _ctx


logger = logging.getLogger(__name__)
BASE_URL = '/api/v2'

app = FastAPI(
    dependencies=[Depends(get_ctx)],
    openapi_url=BASE_URL + "/openapi.json",
    docs_url=BASE_URL + "/docs")
if _ctx.insecure_cors:
    logger.warn("add CORS middleware")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    msg = f"Internal Server Error {type(exc).__name__} {exc}"
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": msg},
    )


@app.on_event("startup")
async def startup_event():
    logger.info(f"Application {__name__} running with base URL {BASE_URL}")


if _ctx.full_access_log:
    @app.middleware("http")
    async def full_access_log(request: Request, call_next):
        response = await call_next(request)
        scope = request.scope
        qh = request.headers
        xff = qh.get("x-forwarded-for", request.client.host)
        referer = qh.get("referer", "no-referer")
        req_info = f"{xff} \"{request.method} {scope['path']} {scope['type']}/{scope['http_version']}\""
        cl = response.headers.get("content-length", "no-content-length")
        resp_info = f"{response.status_code} {cl}"
        req_info_compl = f"\"{referer}\" \"{qh['user-agent']}\""
        logging.getLogger("otvl_web.access").info(f"{req_info} {resp_info} {req_info_compl}")
        return response


@app.get(f"{BASE_URL}/version", status_code=status.HTTP_200_OK)
def get_version():
    return {"version": "2.0.0"}


@app.get(f"{BASE_URL}/echo", status_code=status.HTTP_200_OK)
def echo(
        debug: str = Query(None, description="debug message"),
        info: str = Query(None, description="info message"),
        error: str = Query(None, description="exception message"),
        exception: str = Query(None, description="exception raise with message")
        ):
    res = {}
    if debug:
        res["debug"] = debug
        logger.debug(f"echo {debug}")
    if info:
        res["info"] = info
        logger.info(f"echo {info}")
    if error:
        res["error"] = error
        logger.error(f"echo {error}")
    if exception:
        res["exception"] = exception
        logger.error(f"echo exception {exception}")
        if exception == "OtvlNotImplementedErr":
            raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "echo OtvlNotImplementedErr")
        map = {
            "ValueError": ValueError,
            "NotImplementedError": NotImplementedError
            }
        raise map[exception]()
    return res


@app.get(f"{BASE_URL}/config")
def get_config(ctx=Depends(get_ctx)):
    try:
        config = copy.copy(ctx.config)
        del config["server"]
        return config
    except Exception as ex:
        logger.error(f"Unknown error occurred: {ex}")
        raise HTTPException(status_code=500, detail='Unknown error occurred')


@app.get(f"{BASE_URL}" + "/content/{uri:path}")
def get_content(
        contentFetcher: ContentFetcher = Depends(),
        ctx=Depends(get_ctx)
        ):
    return contentFetcher.fetch(ctx)


@app.get(f"{BASE_URL}" + "/index/{uri:path}")
def get_index(
        indexFetcher: IndexFetcher = Depends(),
        ctx=Depends(get_ctx)
        ):
    return indexFetcher.fetch(ctx)


@app.get(f"{BASE_URL}" + "/html/{uri:path}")
def get_html(
        htmlFetcher: HtmlFetcher = Depends(),
        ctx=Depends(get_ctx)
        ):
    return htmlFetcher.fetch(ctx)


@app.get(f"{BASE_URL}" + "/asset/{uri:path}")
def get_asset(
        uri,
        ctx=Depends(get_ctx)
        ):
    asset_path = f"{ctx.assets_path}/{uri}"
    if os.path.exists(asset_path):
        return FileResponse(asset_path)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.get(f"{BASE_URL}/sitemap.xml")
def get_sitemap(
        request: Request,
        siteMapFetcher: SiteMapFetcher = Depends(),
        ctx=Depends(get_ctx)
        ):
    try:
        return siteMapFetcher.fetch(request, ctx)
    except Exception as ex:
        logger.error(f"Unknown error occurred: {ex}")
        raise HTTPException(status_code=500, detail='Unknown error occurred')
