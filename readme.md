build docker image with
docker build --tag  lordofall/azurefunctionsimage:v1.0.0 .

commit docker with
docker tag lordofall/azurefunctionsimage:v1.0.0 chatwithfriendsregistry.azurecr.io/azurefunctionsimage:v1.0.0

then run docker push
 docker push chatwithfriendsregistry.azurecr.io/azurefunctionsimage:v1.0.0

login to acr
az acr login -n chatwithfriendsregistry -u [UUsername from azure] -p [Passwordfromazure]

az functionapp create --resource-group ChatWithFriendsResourceGroup --consumption-plan-location "brazilsouth" --runtime python --runtime-version 3.10 --functions-version 4 --name chatwithfriendsmvp --storage-account chatwithfriendsdb --os-type linux 

publish with

func azure functionapp publish chatwithfriendsmvp