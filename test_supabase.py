from supabase.lib.client_options import SyncClientOptions
import inspect
print("SyncClientOptions fields:", inspect.signature(SyncClientOptions.__init__))

import httpx
try:
    opts = SyncClientOptions(httpx_client=httpx.Client(verify=False))
    print("httpx_client param OK")
except TypeError as e:
    print(f"httpx_client param FAILED: {e}")
