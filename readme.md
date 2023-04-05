az functionapp create --resource-group ChatWithFriendsResourceGroup --consumption-plan-location "brazilsouth" --runtime python --runtime-version 14 --functions-version 4 --name chatwithfriendsmvp --storage-account chatwithfriendsdb
--os-type linux

publish with

func azure functionapp publish chatwithfriendsmvp