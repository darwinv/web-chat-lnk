
class Client:

    def showClientProfile(request,client_id):
        ObjApi = api(API_CLIENT_ID, API_CLIENT_SECRET, API_URL)
        data = ObjApi.get('clients/'+client_id)
        return render(request, 'admin/detailClient.html',{'data': data})