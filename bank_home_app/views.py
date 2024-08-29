
from django.shortcuts import render,redirect
from .models import Bank,Transaction
from .forms import BankForm,PinForm,MobileForm, OTPForm
from django.contrib import messages

# Create your views here.


def bank(request):
    return render(request,'home.html')

def bank_home(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.set_pin(form.cleaned_data['pin_num'])
            account.save()
            send_mail(
                'Account Created Successfully - R Bank Management System',
                f'Dear {account.first_name},\n\nYour account has been created successfully with R Bank Management System! Your account number is {account.account_number}.',
                'dharaneeshreddy18@gmail.com',  
                [account.email],
                fail_silently=False,
            )
            request.session['account_number'] = account.account_number
            return redirect('account_created')  
    else:
        form = BankForm()
    
    context = {
        'form': form,
    }
    return render(request, 'bank_home.html', context)

def account_created(request):
    account_number = request.session.get('account_number')
    if not account_number:
        return redirect('bank_home')  
    if request.method == 'POST':
        return redirect('2')
    context = {
        'account_number': account_number,
    }
    return render(request, 'account_created.html', context)

def validate_pin(request):
    if request.method == 'POST':
        # if 'forgot_pin' in request.POST:
        #     account_number = request.POST.get('account_num')
        #     try:
        #         account = Bank.objects.get(account_number=account_number)
        #         return redirect('forgotpin', pk=account.pk)
        #     except Bank.DoesNotExist:
        #         messages.error(request, 'Account not found')

        form = PinForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_num']
            pin = form.cleaned_data['pin_num']
            try:
                account = Bank.objects.get(account_number=account_number)
                if account.check_pin(pin):
                    return redirect('3',pk= account.id)
                else:
                    form.add_error('pin_num','Invalid Pin')
            except Bank.DoesNotExist:
                form.add_error('account_num','Account not found')
    else:
        form = PinForm()
    
    context = {
        'form':form,
    }
    
    return render(request,'validate.html',context)

from django.core.mail import send_mail

def forgotpin(request, pk):
    account = Bank.objects.get(id=pk)
    if request.method == 'POST':
        account.generate_otp()  
        send_mail(
        'Your OTP for PIN Reset',
        f'Your OTP is {account.otp}. It is valid for 2 minutes.',
        'dharaneeshreddy18@gmail.com',
        [account.email],
        fail_silently=False,
        )
        request.session['mobile_num'] = account.mobile_num  
        return redirect('validate_otp')
    context = {
        'data': account
    }
    return render(request, 'forgotpin.html', context)

def validate_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        mobile_num = request.session.get('mobile_num')
        if form.is_valid():
            otp = form.cleaned_data['otp']
            new_pin = form.cleaned_data['new_pin']
            try:
                account = Bank.objects.get(mobile_num=mobile_num)
                if account.verify_otp(otp):
                    account.set_pin(new_pin)

                    Transaction.objects.create(
                        account=account,
                        transaction_type='pin_change',
                        amount=0,  
                        description='PIN Change'
                    )

                    del request.session['mobile_num']
                    return redirect('pin_reset_success')
                else:
                    form.add_error('otp', 'Invalid or expired OTP')
            except Bank.DoesNotExist:
                return redirect('forgotpin')
    else:
        form = OTPForm()

    return render(request, 'validate_otp.html', {'form': form})


def pin_reset_success(request):
    return render(request,'pin_reset_success.html')




def userhome(request,pk):
    data = Bank.objects.get(id=pk)
    context = {
        'data':data
    }
   
    return render(request,'userhome.html',context)
        

def withdraw(request, pk):
    data = Bank.objects.get(id=pk)
    message = ''
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            if int(amount) <= data.balance_amount: 
                data.balance_amount -= int(amount)
                data.save()
                
                
                Transaction.objects.create(
                    account=data,
                    transaction_type='withdrawal',
                    amount=int(amount),
                    description='ATM Withdrawal'  
                )
                
                message = "Transaction Successful"
            else:
                message = 'Insufficient Balance'
        except ValueError:
            message = 'Invalid Amount'
    context = {
        'message': message,
        'data': data,
    }
    return render(request, 'withdraw.html', context)

def forgot(request):
    if request.method == 'POST':
        acc = request.POST.get('account')
        # account = Bank.objects.get()
        try:
            account = Bank.objects.get(account_number=acc) 
            return redirect(f'forgotpin/{account.id}')
        except Bank.DoesNotExist:
            messages.error(request, 'Account not found')
        account.generate_otp()  

    return render(request,'forgot.html')

def deposit(request, pk):
    data = Bank.objects.get(id=pk)
    message = ''
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            if int(amount) > 0: 
                data.balance_amount += int(amount)
                data.save()

               
                Transaction.objects.create(
                    account=data,
                    transaction_type='deposit',
                    amount=int(amount),
                    description='ATM Deposit'  
                )
                
                message = "Deposit Successful"
            else:
                message = 'Invalid Amount'
        except ValueError:
            message = 'Invalid Amount'
    
    context = {
        'message': message,
        'data': data,
    }
    return render(request, 'deposit.html', context)


def transfer(request, pk):
    data = Bank.objects.get(id=pk)
    message, message1, message2 = '', '', ''
    if request.method == 'POST':
        acc_ = request.POST.get('account')
        try:
            data1 = Bank.objects.get(account_number=acc_)
            if data1:
                amount = request.POST.get('amount')
                if data.account_number != int(acc_):
                    if int(amount) <= data.balance_amount: 
                        data1.balance_amount += int(amount)
                        data1.save()

                        data.balance_amount -= int(amount)
                        data.save()

                       
                        Transaction.objects.create(
                            account=data,
                            transaction_type='transfer',
                            amount=int(amount),
                            description=f'Transfer to account {data1.account_number}'
                        )
                        Transaction.objects.create(
                            account=data1,
                            transaction_type='deposit',
                            amount=int(amount),
                            description=f'Transfer from account {data.account_number}'
                        )

                        message = 'Transaction Successful'
                    else:
                        message = 'Insufficient Balance'
                else:
                    message1 = 'Unable to transfer to the same account'
        except Bank.DoesNotExist:
            message2 = "Account doesn't exist"
    
    context = {
        'message': message,
        'message1': message1,
        'message2': message2,
        'data': data,
    }

    return render(request, 'transfer.html', context)

def transaction_history(request, pk):
    account = Bank.objects.get(id=pk)
    transactions = account.transactions.all().order_by('-timestamp')
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'transaction_history.html', context)
