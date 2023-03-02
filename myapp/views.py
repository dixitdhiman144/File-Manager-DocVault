from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import os
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
import pandas as pd


# Create your views here.
def index(request):
    
    return render(request, 'user_panel.html')

def admin_panel(request):
    files = []
    folder_path ="uploads/"
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            files.append(filename)
    return render(request,'admin_panel.html', {'files':files})


def login(request):
    #for authantication
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        global auth
        user = (username == 'admin') and (password == 'admin')
        if user:
            return redirect('/try-admin')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('/login')
    else: #for login page
        auth = False
        return render(request, 'login_page.html')

def upload(request):
    try:
        if request.method == 'POST' and request.FILES['file']:
            uploaded_file = request.FILES['file']
            file_name =uploaded_file.name
            file_extension = os.path.splitext(file_name)[1]
            if file_extension == '.csv' or file_extension == '.xlsx':
            #file_name.lower() in ['.csv', '.xlsx']:
                fs = FileSystemStorage(location='uploads/')
                filename = fs.save(uploaded_file.name, uploaded_file)
                messages.info(request,f"File uploaded Successfully : {filename}")
                return redirect('/')
            else: #if file is other then csv and xlsx
                messages.info(request,f"Invalid file type; file type is not .csv or .xlsx Actually file type is {file_extension}")
                return redirect('/')
    except Exception as err: #if we not chose any file
        messages.info(request,"Please Chose a file before upload !!")
        return redirect('/')




def open_file(request):
    folder_path ="uploads/"
    file_name =  request.POST['file']
    # Check if the file exists
    file_path = os.path.join(folder_path, file_name)
    if not os.path.exists(file_path):
        raise Http404
    
    file_extension = os.path.splitext(file_name)[1]
    if file_extension == '.csv':
        # Open the file using pandas because it is a csv file
        df = pd.read_csv(file_path)  # Use pd.read_excel() for Excel files

    else: #file_extension == '.xlsx'
        df = pd.read_excel(file_path, sheet_name='Sheet1')

    # Render the file contents as a table in HTML means converting table to html.
    table_html = df.to_html()

    # Return the table as a Django response
    return HttpResponse(table_html)

def download_file(request):
    folder_path ="uploads/"
    filename =  request.POST['file']
    file_path = os.path.join(folder_path, filename)
    if not os.path.exists(file_path):
        raise Http404

    # Open the file and read its contents
    with open(file_path, 'rb') as f:
        file_contents = f.read()

    # Create a Django response object with the file contents
    response = HttpResponse(file_contents, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response