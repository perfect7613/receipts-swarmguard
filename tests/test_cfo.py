import httpx
import pytest
from receipts.sponsors import CFOClient


def test_authenticated_mcp_handshake_tool_discovery_and_call():
    requests = []
    def handler(request):
        import json
        body = json.loads(request.content)
        requests.append(body)
        assert request.headers["authorization"] == "Bearer test-token"
        if body["method"] == "notifications/initialized":
            return httpx.Response(202)
        if body["method"] == "initialize":
            result = {"protocolVersion": "2025-03-26", "capabilities": {}, "serverInfo": {"name": "test", "version": "1"}}
        elif body["method"] == "tools/list":
            assert request.headers["mcp-session-id"] == "session-test"
            result = {"tools": [{"name": "inspect_pages", "inputSchema": {"type": "object"}}]}
        else:
            result = {"content": [{"type": "text", "text": "ok"}]}
        return httpx.Response(200, headers={"mcp-session-id": "session-test"},
                              json={"jsonrpc": "2.0", "id": body["id"], "result": result})
    client = CFOClient("test-token", httpx.Client(transport=httpx.MockTransport(handler)))
    assert client.call("inspect_pages", {"list": {}, "org_id": "workspace-test"})["content"][0]["text"] == "ok"
    assert [r["method"] for r in requests] == ["initialize", "notifications/initialized", "tools/list", "tools/call"]
    with pytest.raises(ValueError, match="not published"):
        client.call("invented_tool", {})
    client.close()


def test_auth_failure_does_not_expose_token_or_response_body():
    client = CFOClient("sensitive-test-token", httpx.Client(transport=httpx.MockTransport(
        lambda request: httpx.Response(401, text="sensitive-test-token"))))
    with pytest.raises(ValueError, match="HTTP 401") as exc:
        client.tools()
    assert "sensitive-test-token" not in str(exc.value)
    client.close()
