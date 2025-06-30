from converter.components.client_wrapper import BritiveClientWrapper
import os

tenant = os.getenv("BRITIVE_TENANT", "courage.dev2.aws")
client_wrapper = BritiveClientWrapper(tenant)

