from converter_config.base import ToolConfig, ToolGroup

security_active_session = ToolGroup(
    name="security.active_sessions",
    tools=[
        ToolConfig(
            function_name="list_users",
            ai_description="Lists all users on the Britive platform with active sessions in applications or resources. Returns user details including userId, name, userType, email, username, countOfProfiles, and lastLogin. Use this tool to search for a user and retrieve their userId, which can be used in follow-up operations such as retrieving the Profile Application ID (papID).",         
            regenerate=True
            ),
        ToolConfig(
            function_name="list_user_sessions",
            ai_description="This tool list all active session i.e. checkedout profiles for a user in the Britive platform. It returns details such as papId, profileName, description, transactionId, status, checkedOut, expiration, environmentID, EnvironmentName, accessType, appContainerId, appName, appType as part of applications list. Use this tool once you get userId and from that userId you will get all profiles associated with that user. Use this tool after obtaining the userId to fetch all profiles currently checked out by the user. This is typically used before invoking checkin or checkin_all operations to identify which sessions are active",         
            regenerate=True
            ),
        ToolConfig(
            function_name="checkin",
            ai_description="This Tool will take userId and list of papID i.e. profile application ID and checkin the profile application ID for the user. It will return a message indicating whether the check-in was successful or if there were any issues.",         
            regenerate=True
            ),
        ToolConfig(
            function_name="checkin_all",
            ai_description="This tool checks in all active sessions for a specific user. It requires the userId to identify the user whose sessions should be checked in. The tool will return a message indicating whether the check-in was successful or if there were any issues.",         
            regenerate=True
            ),
    ]
)