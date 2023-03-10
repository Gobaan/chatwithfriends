Initially followed this tutorial

https://learn.microsoft.com/en-us/azure/azure-web-pubsub/quickstart-serverless?tabs=javascript

Used this to create runtime

az functionapp create --resource-group ChatWithFriendsResourceGroup --consumption-plan-location "brazilsouth" --runtime python --runtime-version 3.10 --functions-version 4 --name chatwithfriendsmvp --storage-account chatwithfriendsdb
--os-type linux

Used this tutorial to convert code to python

https://techcommunity.microsoft.com/t5/apps-on-azure-blog/tutorial-azure-web-pubsub-trigger-for-azure-python-functions/ba-p/3650727

Critical for new projects:
Remember to set WebPubSubConnectionString, create an event handler, and enable client authentication


testing:

first start blob storage.

f1, azurite start table storage service
then in terminal type
> func start 

go to urls
