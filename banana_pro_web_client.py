#!/usr/bin/env python3
"""
Banana Pro Web Automation Client

A stable client for xais1.dchai.cn that mimics the web app request flow:
1. xtoken login
2. fetch model config
3. start worker task
4. wait on SSE task stream
5. resolve image URLs and download
"""

from __future__ import annotations

import json
import secrets
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Literal, Optional

import requests


class BananaProWebClient:
    """Client for Banana Pro generation via xais web endpoints."""

    REQUEST_ID_CHARS = "useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict"

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://xais1.dchai.cn",
        timeout: int = 30,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self._logged_in = False
        self._conf_cache: Optional[Dict[str, Any]] = None

    def _request_id(self, length: int = 10) -> str:
        return "".join(
            self.REQUEST_ID_CHARS[b & 63] for b in secrets.token_bytes(length)
        )

    def _request(
        self,
        method: Literal["GET", "POST"],
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json_body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        stream: bool = False,
        timeout: Optional[int] = None,
    ) -> requests.Response:
        req_headers = {"x-request-id": self._request_id()}
        if headers:
            req_headers.update(headers)

        resp = self.session.request(
            method,
            f"{self.base_url}{path}",
            params=params,
            data=data,
            json=json_body,
            headers=req_headers,
            stream=stream,
            timeout=timeout or self.timeout,
        )
        resp.raise_for_status()
        return resp

    def login(self, force: bool = False) -> Dict[str, Any]:
        """Login with xtoken (api_key) and initialize session cookies."""
        if self._logged_in and not force:
            profile = self.user_profile()
            if profile:
                return profile

        resp = self._request(
            "POST",
            "/xais/xtokenLogin",
            data=self.api_key,
            headers={"content-type": "text/plain"},
        )
        profile = resp.json()
        self._logged_in = True
        return profile

    def ensure_login(self) -> None:
        if not self._logged_in:
            self.login()

    def user_profile(self) -> Dict[str, Any]:
        self.ensure_login()
        return self._request("GET", "/xais/userProfile").json()

    def conf_get(self, refresh: bool = False) -> Dict[str, Any]:
        self.ensure_login()
        if self._conf_cache is not None and not refresh:
            return self._conf_cache
        self._conf_cache = self._request("GET", "/xais/confGet").json()
        return self._conf_cache

    def list_models(self) -> Dict[str, Any]:
        conf = self.conf_get()
        models = conf.get("ALL_MODELS", [])
        return {"data": models, "default": conf.get("DEFAULT_MODEL")}

    def _resolve_model(self, route: str) -> str:
        if route.startswith("Nano_Banana_Pro_"):
            return route
        if route.startswith(("2K_", "4K_")):
            return f"Nano_Banana_Pro_{route}"
        return route

    def _route_from_model(self, model_name: str) -> str:
        if model_name.startswith("Nano_Banana_Pro_"):
            return model_name.replace("Nano_Banana_Pro_", "")
        return model_name

    def _candidate_models(self, route: str) -> list[str]:
        requested = self._resolve_model(route)
        conf = self.conf_get()
        all_models = [m.get("name") for m in conf.get("ALL_MODELS", []) if m.get("name")]

        # Stable fallback order from real-world usage: 2/5 first, then the rest.
        if requested.startswith("Nano_Banana_Pro_2K_"):
            preferred = [
                "Nano_Banana_Pro_2K_2",
                "Nano_Banana_Pro_2K_5",
                "Nano_Banana_Pro_2K_1",
                "Nano_Banana_Pro_2K_3",
                "Nano_Banana_Pro_2K_4",
                "Nano_Banana_Pro_2K_6",
                "Nano_Banana_Pro_2K_7",
            ]
        elif requested.startswith("Nano_Banana_Pro_4K_"):
            preferred = [
                "Nano_Banana_Pro_4K_2",
                "Nano_Banana_Pro_4K_5",
                "Nano_Banana_Pro_4K_1",
                "Nano_Banana_Pro_4K_3",
                "Nano_Banana_Pro_4K_4",
                "Nano_Banana_Pro_4K_6",
                "Nano_Banana_Pro_4K_7",
            ]
        else:
            preferred = [requested]

        candidates: list[str] = []
        for name in [requested] + preferred:
            if name in all_models and name not in candidates:
                candidates.append(name)

        if not candidates:
            candidates.append(requested)
        return candidates

    def _resolve_ratio(self, model_name: str, aspect_ratio: str) -> str:
        conf = self.conf_get()
        default_model = conf.get("DEFAULT_MODEL") or {}
        all_models = conf.get("ALL_MODELS") or []

        selected = next((m for m in all_models if m.get("name") == model_name), None)
        if not selected:
            if default_model.get("name"):
                return default_model.get("defaultRatio", "1:1")
            return "1:1"

        ratios = selected.get("ratios") or []
        if not ratios:
            return aspect_ratio
        if aspect_ratio in ratios:
            return aspect_ratio
        return selected.get("defaultRatio") or ratios[0]

    def _start_task(self, prompt: str, model: str, ratio: str) -> str:
        payload = {
            "prompt": prompt,
            "model": model,
            "ratio": ratio,
            "client": "XAIS",
        }
        resp = self._request(
            "POST",
            "/xais/workerTaskStart",
            json_body=payload,
            headers={"content-type": "application/json"},
        )
        return resp.text.strip().strip('"')

    def _wait_task(
        self,
        task_id: str,
        timeout: int = 240,
    ) -> Dict[str, Any]:
        deadline = time.time() + timeout
        last_msg = None

        resp = self._request(
            "GET",
            "/xais/workerTaskWait",
            params={"id": task_id},
            headers={"accept": "text/event-stream"},
            stream=True,
            timeout=timeout,
        )

        with resp:
            for raw_line in resp.iter_lines():
                if time.time() > deadline:
                    raise TimeoutError(f"Task wait timeout after {timeout}s")
                if not raw_line:
                    continue

                line = raw_line.decode("utf-8", errors="ignore")
                if not line.startswith("data: "):
                    continue

                data = line[6:]
                try:
                    obj = json.loads(data)
                except json.JSONDecodeError:
                    continue

                if "msg" in obj:
                    last_msg = obj["msg"]
                if "result" in obj:
                    return {
                        "task_id": task_id,
                        "result": obj["result"],
                        "progress": obj.get("progress"),
                        "last_msg": last_msg,
                    }
                if "error" in obj:
                    raise RuntimeError(f"Task failed: {obj['error']}")

        raise RuntimeError("Task stream ended without result")

    def _att_urls(self, attachment: str) -> Dict[str, Any]:
        resp = self._request("GET", "/xais/attUrls", params={"att": attachment})
        return resp.json()

    def _download_image(self, image_url: str, save_path: str) -> str:
        save_file = Path(save_path)
        save_file.parent.mkdir(parents=True, exist_ok=True)

        resp = self.session.get(image_url, timeout=self.timeout)
        resp.raise_for_status()

        with open(save_file, "wb") as f:
            f.write(resp.content)
        return str(save_file)

    def generate_image(
        self,
        prompt: str,
        route: str = "2K_2",
        aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:2", "4:5", "21:9"] = "1:1",
        save_path: Optional[str] = None,
        retries: int = 2,
        wait_timeout: int = 240,
    ) -> Dict[str, Any]:
        """Generate one image through web task endpoints and save it locally."""
        self.ensure_login()

        model_candidates = self._candidate_models(route)

        last_err: Optional[Exception] = None
        for model_name in model_candidates:
            resolved_ratio = self._resolve_ratio(model_name, aspect_ratio)
            for attempt in range(1, retries + 2):
                try:
                    task_id = self._start_task(prompt=prompt, model=model_name, ratio=resolved_ratio)
                    task_result = self._wait_task(task_id=task_id, timeout=wait_timeout)

                    attachments = task_result.get("result") or []
                    if not attachments:
                        raise RuntimeError("No image attachment returned")

                    attachment = attachments[0]
                    urls = self._att_urls(attachment)
                    image_url = urls.get("download") or urls.get("webp") or urls.get("thumb")
                    if not image_url:
                        raise RuntimeError(f"No downloadable URL in attUrls response: {urls}")

                    if save_path is None:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        actual_route = self._route_from_model(model_name)
                        save_path = f"banana_pro_web_{actual_route}_{timestamp}.png"

                    saved_to = self._download_image(image_url, save_path)
                    return {
                        "task_id": task_id,
                        "model": model_name,
                        "route": self._route_from_model(model_name),
                        "aspect_ratio": resolved_ratio,
                        "attachment": attachment,
                        "image_url": image_url,
                        "saved_to": saved_to,
                        "raw": {
                            "task_result": task_result,
                            "att_urls": urls,
                        },
                    }
                except Exception as err:
                    last_err = err
                    if attempt > retries:
                        break
                    # transient network / task failures often recover on one retry
                    time.sleep(2)

        raise RuntimeError(f"Image generation failed after retries: {last_err}")


def main() -> None:
    """Quick manual test."""
    api_key = "sk-your-key"
    client = BananaProWebClient(api_key=api_key)

    print("Testing web automation flow...")
    profile = client.login()
    print(f"Logged in user id: {profile.get('id')}")

    result = client.generate_image(
        prompt="A red apple on white background, photorealistic",
        route="2K_2",
        aspect_ratio="1:1",
    )
    print(f"Image saved: {result['saved_to']}")


if __name__ == "__main__":
    main()
