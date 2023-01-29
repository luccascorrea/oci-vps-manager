from app import OCIStatusBarApp
from services import (
    InstanceStatusService,
    InstanceStartService,
    InstanceStopService,
    CurrentSpendService,
)

if __name__ == "__main__":
    OCIStatusBarApp(
        name="VPS",
        instance_status_service=InstanceStatusService(),
        instance_start_service=InstanceStartService(),
        instance_stop_service=InstanceStopService(),
        current_spend_service=CurrentSpendService(),
    ).run()
