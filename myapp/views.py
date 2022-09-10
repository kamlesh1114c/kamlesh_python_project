from django.shortcuts import render,redirect
from .models import Contact,User,Doctor_Profile,Appointment,CancelAppointment,HealthProfile,Transaction
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
# Create your views here.

def index(request):
	return render(request,'index.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			address=request.POST['address'],
		)
		msg="Contact Saved Successfully"
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render (request,'contact.html',{'msg':msg,'contacts':contacts})
	else:
		
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'contacts':contacts})

def gallery(request):
	return render (request,'gallery.html')

def about(request):
	return render (request,'about.html')

def signup(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					name=request.POST['name'],
					email=request.POST['email'],
					password=request.POST['password'],
					)
				msg="Sign Up Successfully"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="Password And Confirm password Does Not Matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')	

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'],
				password=request.POST['password'])
			if user.usertype=="patient":
				request.session['email']=user.email
				request.session['name']=user.name
				appointments=Appointment.objects.filter(patient=user,status="pending")
				request.session['appointment_count']=len(appointments)
				msg="Login Successfully"
				return render(request,'index.html',{'msg':msg})
			else:
				request.session['email']=user.email
				request.session['name']=user.name
				return render(request,'doctor_index.html')
				
		except Exception as e:
			print(e)
			msg="Email or Password Is Incorrect"
			return render (request,'login.html',{'msg':msg})
	else:				
		return render (request,'login.html')
	
def logout(request):
	try:
		del request.session['email']
		del request.session['name']
		return render (request,'login.html')
	except:
		return render(request,'login.html')
	
def doctor_profile(request):
	doctor_profile=Doctor_Profile()
	doctor=User.objects.get(email=request.session['email'])
	try:
		doctor_profile=Doctor_Profile.objects.get(doctor=doctor)
	except:
		pass
	if request.method=="POST":	
		if doctor_profile.doctor_specialitiy:
			doctor_profile.doctor=doctor
			doctor_profile.doctor_degree=request.POST['doctor_degree']
			doctor_profile.doctor_specialitiy=request.POST['doctor_specialitiy']
			doctor_profile.doctor_start_time=request.POST['doctor_start_time']
			doctor_profile.doctor_end_time=request.POST['doctor_end_time']
			doctor_profile.doctor_fees=request.POST['doctor_fees']
			try:
				doctor_profile.doctor_picture=request.FILES['doctor_picture']
			except:
				pass
			doctor_profile.save()
			msg="doctor Profile Updated Successfully"
			return render(request,'doctor_profile.html',{'doctor_profile':doctor_profile,'msg':msg})
	
	else:			
		if request.method=="POST":
			doctor=Doctor_Profile.objects.create(
				doctor=doctor,
				doctor_degree=request.POST['doctor_degree'],
				doctor_specialitiy=request.POST['doctor_specialitiy'],
				doctor_start_time=request.POST['doctor_start_time'],
				doctor_end_time=request.POST['doctor_end_time'],
				doctor_fees=request.POST['doctor_fees'],
				doctor_picture=request.FILES['doctor_picture'])

			msg="doctor Profile Created Successfully"
			return render(request,'doctor_profile.html',{'doctor_profile':doctor_profile,'msg':msg})

		else:	
			return render(request,'doctor_profile.html',{'doctor_profile':doctor_profile})

def doctors(request):
	doctors=Doctor_Profile.objects.all()
	return render(request,'doctors.html',{'doctors':doctors})				

def doctor_detail(request,pk):
	doctor=Doctor_Profile.objects.get(pk=pk)
	return render(request,'doctor_detail.html',{'doctor':doctor})

def book_appointment(request,pk):
	doctor=Doctor_Profile.objects.get(pk=pk)
	patient=User.objects.get(email=request.session['email'])

	if request.method=="POST":
		appointment=Appointment.objects.create(
				patient=patient,
				doctor=doctor,
				date=request.POST['date'],
				time=request.POST['time'],
				health_issu=request.POST['health_issu']
			)
		msg="Appointment Book Successfully"
		appointments1=Appointment.objects.filter(patient=patient,status="pending")
		request.session['appointment_count']=len(appointments1)
		appointments=Appointment.objects.filter(patient=patient)
		#return render(request,'myappointment.html',{'msg':msg,'appointments':appointments})
		return render (request,'paytm.html',{'appointment':appointment})
	else:
		return render(request,'book_appointment.html',{'doctor':doctor,'patient':patient})

def myappointment(request):
	patient=User.objects.get(email=request.session['email'])
	appointments=Appointment.objects.filter(patient=patient)
	appointments1=Appointment.objects.filter(patient=patient,status="pending")
	request.session['appointment_count']=len(appointments1)
	return render(request,'myappointment.html',{'appointments':appointments})

def patient_cancel_appointment(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	if request.method=="POST":
		CancelAppointment.objects.create(
				appointment=appointment,
				reason=request.POST['reason'] 
			)
		appointment.status="Cancelled by patient"
		appointment.save()
		return redirect("myappointment")
	else:	
		return render(request,'patient_cancel_appointment.html',{'appointment':appointment})


def health_profile(request):
	health_profile=HealthProfile()
	patient=User.objects.get(email=request.session['email'])
	try:
		health_profile=HealthProfile.objects.get(patient=patient)
	except:
		pass	
	if request.method=="POST":
		diabetes=request.POST['diabetes']
		if diabetes=="yes":
			flag1=True 
		else:
			flag1=False
		blood_pressure=request.POST['blood_pressure']
		if blood_pressure=="yes":
			flag2=True 
		else:
			flag2=False
		health_profile=HealthProfile.objects.create(
			patient=patient,
			blood_group=request.POST['blood_group'],
			weight=request.POST['weight'],
			diabetes=flag1,
			blood_pressure=flag2,
		)
		msg="Health Profile Updated successully"
		return render(request,'health_profile.html' ,{'msg':msg,'health_profile':health_profile})
	else:	
		return render(request,'health_profile.html',{'health_profile':health_profile})			


def my_appointment(request):
	doctor=User.objects.get(email=request.session['email'])
	doctor_profile=Doctor_Profile.objects.get(doctor=doctor)
	doctor_appointment=Appointment.objects.filter(doctor=doctor_profile)
	return render(request,'my_appointment.html',{'doctor_appointment':doctor_appointment})

def doctor_index(request):
	return render(request,'doctor_index.html')

def doctor_approve_appointment(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	appointment.status="approved"
	appointment.save()
	return redirect('my_appointment')

def doctor_complete_appointment(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	if request.method=="POST":
		appointment.prescription=request.POST['prescription']
		appointment.status="completed"
		appointment.save()
		return redirect('my_appointment')

	else:
		return render(request,'doctor_complete_appointment.html',{'appointment':appointment})
		
	#appointment.status="completed"
	#appointment.save()

def doctor_cancel_appointment(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	appointment.status="cancelled By Doctor"
	appointment.save()
	return redirect('my_appointment')


def initiate_payment(request):
    user=User.objects.get(email=request.session['email'])
    pk=int(request.POST['pk'])
    try:

        amount = int(request.POST['amount'])
    except:
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user,amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(user.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    appointment=Appointment.objects.get(pk=pk)
    appointment.payment_status="paid"
    appointment.save()
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
	if request.method == 'POST':
		received_data = dict(request.POST)
		paytm_params = {}
		paytm_checksum = received_data['CHECKSUMHASH'][0]
		for key, value in received_data.items():
			if key == 'CHECKSUMHASH':
				paytm_checksum = value[0]
			else:
				paytm_params[key] = str(value[0])
        # Verify checksum
		is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
		if is_valid_checksum:
			received_data['message'] = "Checksum Matched"
		else:
			received_data['message'] = "Checksum Mismatched"
			return render(request, 'callback.html', context=received_data)
		return render(request, 'callback.html', context=received_data)


def validate_email(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

def validate_appointment(request):
	appointment=request.GET.get('appointment')
	data={
		'is_taken':Appointment.objects.filter(date__iexact=appointment).exists()
	}
	print(data)
	return JsonResponse(data)

def validate_appointment_time(request):
	appointment=request.GET.get('appointment')
	data={
		'is_taken':Appointment.objects.filter(time__iexact=appointment).exists()
	}
	print(data)
	return JsonResponse(data)	