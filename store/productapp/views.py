from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from productapp.sort import sort_index,sort_secindex

from productapp.forms import UserProfileInfoForm,LoginForm,AddProduct,Search,SearchByName

# function for signup.
def register(request):
	if request.method == "POST":
		profile_form = UserProfileInfoForm(data=request.POST)
		if profile_form.is_valid():
			with open("accounts.txt", "r") as file:
				data = file.readlines()
				for line in data:
					data_info = line.split(" ")
					if profile_form.cleaned_data['username'] == data_info[0]:
						messages.success(request,('Username already exists'))
						return redirect("productapp:signup")
			with open("accounts.txt","a") as file:
				file.write(profile_form.cleaned_data['username'])
				file.write(" ")
				file.write(profile_form.cleaned_data['email'])
				file.write(" ")
				file.write(profile_form.cleaned_data['password'])
				file.write("\n")
			request.session['username'] = profile_form.cleaned_data['username']
			return redirect("productapp:hello")
	else:
		profile_form = UserProfileInfoForm()
	return render(request,"productapp/index.html", {'profile_form':profile_form})


def login(request):
	if request.method == "POST":
		login_form = LoginForm(data=request.POST)
		if login_form.is_valid():
			with open("accounts.txt","r") as file:
				for line in file.readlines():
					login_info = line.split()
					if login_form.cleaned_data['username'] == login_info[0] and login_form.cleaned_data['password'] == login_info[2]:
						request.session['username'] = login_form.cleaned_data['username']
						return redirect("productapp:hello")
				else:
					messages.success(request,('Username/Password Incorrect'))
					return redirect("productapp:login")
	else:
		login_form = LoginForm()
	return render(request,"productapp/login.html", {'login_form':login_form})


def hello(request):
	login1 = request.session['username']
	if login1:
		return render(request,"productapp/hello.html")
	else:
		return redirect("productapp:login")


def logout(request):
	del request.session['username']
	return redirect("productapp:login")


def add_product(request):
	if request.method == "POST":
		product_form = AddProduct(data=request.POST)
		index = None
		if product_form.is_valid():
			pname = str(product_form.cleaned_data['pname'])
			pname = pname.split(" ")
			pname = "-".join(pname)
			pid = str(product_form.cleaned_data['pid'])
			with open("product.txt","r") as file:
				for line in file:
					arr = line.split(" ")
					if pid == arr[1]:
						messages.success(request,('Item Already Exists'))
						return redirect("productapp:add")
					index = int(arr[0])
			with open("product.txt","a") as file:
				if index is None:
					index = 0
				else:
					index = index + 1
				file.write(str(index))
				file.write(" ")
				file.write((str(product_form.cleaned_data['pid'])).upper())
				file.write(" ")
				file.write(pname.upper())
				file.write(" ")
				file.write(str(product_form.cleaned_data['quantity']))
				file.write(" ")
				file.write(str(product_form.cleaned_data['price']))
				file.write("\n")
			with open("index.txt","a") as file:
				file.write(str(index))
				file.write(" ")
				file.write((str(product_form.cleaned_data['pid'])).upper())
				file.write("\n")
			with open("secindex.txt","a") as file:
				file.write((str(product_form.cleaned_data['pid'])).upper())
				file.write(" ")
				file.write(pname.upper())
				file.write("\n")
			
			#sorting index on basis of primary key
			sort_index()
			sort_secindex()
			messages.success(request,('Item has been Added'))
			return redirect("productapp:view_all")
	else:
		product_form = AddProduct()
	return render(request,"productapp/add_product.html", {'product_form':product_form})


def search_product(request):
	if request.method == "POST":
		search_product = Search(data=request.POST)
		if search_product.is_valid():
			pid = (str(search_product.cleaned_data['pid'])).upper()
			p_id = pid+"\n"
			with open("index.txt","r") as file1:
				for line in file1:
					arr1 = line.split(" ")
					if p_id == arr1[1]:
						index = arr1[0]
						break
				else:
					messages.success(request,('No Item Exists'))
					return redirect("productapp:search")
			with open("product.txt","r") as file:
				for line in file:
					arr = line.split(" ")
					if index == arr[0]:
						return render(request,"productapp/view.html",{'arr':arr})
	else:
		search_product = Search()
	return render(request,"productapp/search.html", {'search_product':search_product})


def search_by_name(request):
	if request.method == "POST":
		search_name = SearchByName(data=request.POST)
		if search_name.is_valid():
			search_data = []
			pname = (search_name.cleaned_data['pname']).upper()
			pname = pname.split(" ")
			pname = "-".join(pname)
			with open("secindex.txt","r") as secfile:
				for line in secfile:
					data = line.split(" ")
					if pname in data[1]:
						new_data = data[0]+"\n"
						search_data.append(new_data)
				if len(search_data)<1:
					messages.success(request,('No Item Exists'))
					return redirect("productapp:search_by_name")		
			
			with open("index.txt","r") as indfile:
				index_data = []
				
				for line in indfile:
					data = line.split(" ")
					pid = data[1]
					if pid in search_data:
						index_data.append(data[0])
				
			with open("product.txt", "r") as productfile:
				product_data = []
				for line in productfile:
					data = line.split(" ")
					index = data[0]
					if index in index_data:
						product_data.append(data)
			return render(request,"productapp/view_all.html",{'rows':product_data})




	else:
		search_name = SearchByName()
	return render(request,"productapp/search_by_name.html", {'search_name':search_name})

def view_product(request):
	return render(request,"productapp/view.html")


def view_all(request):
	rows = []
	with open("product.txt","r") as file:
		for line in file:
			row = line.split(" ")
			rows.append(row)
	rows = sorted(rows, key = lambda x: x[2])
	return render(request,"productapp/view_all.html",{'rows':rows})


def delete_product(request,pid):
	with open("product.txt", "r+") as f:
		d = f.readlines()
		f.seek(0)
		for i in d:
			i = i.split(" ")
			if i[1] != pid:
				i = " ".join(i)
				f.write(i)
		f.truncate()
	with open("index.txt", "r+") as f:
		d = f.readlines()
		f.seek(0)
		for i in d:
			i = i.split(" ")
			p_id = pid+"\n"
			if i[1] != p_id:
				i = " ".join(i)
				f.write(i)
		f.truncate()
	with open("secindex.txt", "r+") as f:
		d = f.readlines()
		f.seek(0)
		for i in d:
			i = i.split(" ")
			if i[0] != pid:
				i = " ".join(i)
				f.write(i)
		f.truncate()
	sort_index()
	sort_secindex()
	
	messages.success(request,('Item has been deleted'))
	return redirect('productapp:view_all')


def update_product(request,pid):

	if request.method == "POST":
		pid1 = request.POST.get('pid')
		pname = request.POST.get('pname')
		pname = pname.split(" ")
		pname = "-".join(pname)
		quantity = request.POST.get('quantity')
		price = request.POST.get('price')

		with open("product.txt","r") as file:
			for line in file:
				arr1 = line.split(" ")
				if pid == arr1[1]:
					arr1 = line.split(" ")
					break
		
		with open("product.txt", "r") as file:
			data = file.readlines()
			new_data = []
			index_data = []
			secindex_data = []
			for line in data:
				arr = line.split(" ")
				if arr[1] == pid1 and arr[1] != pid:
					messages.success(request,('Product Id already exists'))
					return render(request,"productapp/update.html",{'arr':arr1})

				if arr[1] == pid:
					line = arr[0]+" "+pid1.upper()+" "+pname.upper()+" "+quantity+" "+price+"\n"
					index = arr[0]+" "+pid1.upper()+"\n"
					secindex = pid1.upper()+" "+pname.upper()+"\n"
					new_data.append(line)
					index_data.append(index)
					secindex_data.append(secindex)
				else:
					new_data.append(line)
					index = arr[0]+" "+arr[1].upper()+"\n"
					secindex = arr[1].upper()+" "+arr[2].upper()+"\n"
					index_data.append(index)
					secindex_data.append(secindex)
			
		with open("product.txt", "w") as file:
			file.writelines(new_data)
		with open("index.txt", "w") as file:
			file.writelines(index_data)
		with open("secindex.txt", "w") as file:
			file.writelines(secindex_data)
		sort_index()
		sort_secindex()
		messages.success(request,('Item has been Updated'))
		return redirect("productapp:view_all")


	with open("product.txt","r") as file:
		for line in file:
			arr1 = line.split(" ")
			if pid == arr1[1]:
				return render(request,"productapp/update.html",{'arr':arr1})
		else:
			messages.success(request,('No Item Exists'))
			return redirect("productapp:search")







		