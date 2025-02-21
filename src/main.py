from asyncio import sleep
import json
import random

from litestar import Litestar, get, post
from litestar.config.cors import CORSConfig
from litestar.connection import Request
from litestar.response import Response
from pydantic import BaseModel, ValidationError, field_validator
from datetime import date


class SubmitRequest(BaseModel):
    date: date
    first_name: str
    last_name: str

    @field_validator("first_name", "last_name")
    def no_spaces(cls, value):
        if " " in value:
            raise ValueError("No whitespace allowed")
        return value


@get("/")
async def index() -> Response:
    return Response(
        content="""
        <html>
        <head><title>HTMX App</title></head>
        <body>
            <h1>Welcome</h1>
            <a href="/form">Go to form</a>
        </body>
        </html>
        """,
        media_type="text/html",
    )


FORM_PAGE_1 = """
<html>
<head>
    <script src="https://unpkg.com/htmx.org@1.9.6"></script>
    <script src="https://unpkg.com/htmx.org/dist/ext/json-enc.js"></script>
    <script src="https://unpkg.com/htmx-ext-response-targets@2.0.0/response-targets.js"></script>
    <style>
        #spinner {
            visibility: hidden;
            border: 5px solid rgba(255, 87, 51, 0.2);
            border-top: 5px solid #FF5733;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 2s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <h1>Form Page</h1>
    <div hx-ext="response-targets">
        <form hx-post="/api/submit"
            hx-target="#result"
            hx-ext="json-enc"
            hx-indicator="#spinner"
            hx-target-error="#result"
            hx-on::after-request="updateURL(event)"
            hx-on::before-request="clearMessages()">
            <label>Date: <input type="date" name="date" required></label><br>
            <label>First Name: <input type="text" name="first_name" required></label><br>
            <label>Last Name: <input type="text" name="last_name" required></label><br>
            <button type="submit">Submit</button>
        </form>
        <div id="spinner"></div>
        <pre id="result">"""


FORM_PAGE_2 = """</pre>
        <script>
            function clearMessages() {
                document.getElementById("result").innerHTML = "";
            }
            document.addEventListener('htmx:afterSwap', (event) => {
                if (event.target.id === "result") {
                    const response = event.detail.xhr.response;
                    if (JSON.parse(response).error) {
                        const errors = JSON.parse(response).error;
                        document.getElementById("result").innerHTML = JSON.stringify(errors, null, 2)
                    } else {
                        const data = JSON.parse(response).data;
                        document.getElementById("result").innerHTML = JSON.stringify(data, null, 2)
                    }
                }
            });
            function updateURL(event) {
                if (event.detail.successful) {
                    const formData = new FormData(document.querySelector("form"));
                    const params = new URLSearchParams(formData).toString();
                    window.history.pushState({}, "", "?" + params);
                }
            }
            function restoreFormFromURL() {
                const params = new URLSearchParams(window.location.search);
                document.querySelector("input[name='date']").value = params.get("date") || "";
                document.querySelector("input[name='first_name']").value = params.get("first_name") || "";
                document.querySelector("input[name='last_name']").value = params.get("last_name") || "";
            }
            document.addEventListener("DOMContentLoaded", restoreFormFromURL);
            document.addEventListener("htmx:beforeRequest", function() {
                document.getElementById("spinner").style.visibility = "visible";
            });
            document.addEventListener("htmx:afterRequest", function() {
                document.getElementById("spinner").style.visibility = "hidden";
            });
        </script>
    </div>
</body>
</html>
"""


def prepare_data(data: dict[str, str]) -> dict[str, str]:
    try:
        form_data = SubmitRequest(**data)
    except ValidationError as e:
        errors = {err["loc"][0]: str([err["msg"]]) for err in e.errors()}
        return {"success": False, "error": errors}

    response_data = [
        {
            "date": form_data.date.strftime("%Y-%m-%d"),
            "name": f"{form_data.first_name} {form_data.last_name}",
        }
        for _ in range(random.randint(2, 5))
    ]
    return {"success": True, "data": response_data}


@get("/form")
async def form_page(request: Request) -> Response:
    if not request.query_params:
        return Response(
            content=f"{FORM_PAGE_1}{FORM_PAGE_2}",
            media_type="text/html",
        )

    result = prepare_data(dict(request.query_params))

    if not result["success"]:
        json_str = json.dumps(result["error"], indent=2)
        return Response(
            content=f"{FORM_PAGE_1}{json_str}{FORM_PAGE_2}",
            media_type="text/html",
            status_code=400,
        )

    json_str = json.dumps(result["data"], indent=2)
    return Response(
        content=f"{FORM_PAGE_1}{json_str}{FORM_PAGE_2}",
        media_type="text/html",
    )


@post("/api/submit")
async def submit(data: dict[str, str]) -> Response:
    await sleep(random.uniform(0, 2.5))

    result = prepare_data(data)

    if not result["success"]:
        return Response(
            content=result,
            status_code=400,
        )
    return Response(
        content=result,
    )


cors_config = CORSConfig(allow_origins=["*"])

app = Litestar(
    route_handlers=[index, form_page, submit],
    cors_config=cors_config,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
