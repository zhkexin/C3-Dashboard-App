import requests
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404 
from django.forms import inlineformset_factory
from django.db.models import Count
from .models import Claim, Problem, Sale, ClaimReport, Work_order_form 
from .forms import ClaimForm, ProblemForm, Work_order_form_form 
from .claimimageuploads import handle_uploaded_files
import csv
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404



############################################################################ HOME ############################################################################
def index(request):
    """The home page for web_app."""
    return render(request, 'web_app/index.html') ########### NOTE: this probably need to change once authorization gets added with the proper webpages ###########


############################################################################ SALES ############################################################################
@login_required
@permission_required("web_app.view_sale")
def work_order_forms(request):
    # Make sure the topic belongs to the current user.
    """show all work Order Forms"""
    print('work_order_forms view function called')
    work_order_form_list=Work_order_form.objects.order_by('date_added')     # creates a list of all work order forms
    context={'work_order_forms':work_order_form_list}                       # assigns context as the list of work order forms 
    return render(request,'web_app/work_order_forms.html',context)

@login_required
@permission_required("web_app.view_sale")
def work_order_form(request, work_order_form_number):
    """Show a single Work Order Form."""
    # Make sure that the Work_order_form object exists in the database
    myWorkOrderForm = get_object_or_404(Work_order_form, work_order_form_number=work_order_form_number)

    context = {'work_order_form': myWorkOrderForm}
    return render(request, 'web_app/work_order_form.html', context)

@login_required
@permission_required("web_app.view_sale")
def new_work_order_form(request):
    """Add a new work order form."""
    if request.method == 'POST':
        form = Work_order_form_form(request.POST)
        if form.is_valid():
            work_order_form = form.save(commit=False)
            work_order_form.work_order_form_number = Work_order_form.objects.count() + 1  # manually increment form number
            work_order_form.save()
            return redirect('web_app:work_order_forms')
    else:
        form = Work_order_form_form()
        # Set the initial value of the work_order_form_number field
        form.fields['work_order_form_number'].initial = Work_order_form.objects.last().work_order_form_number + 1
        # Set the work_order_form_number field as read-only
        form.fields['work_order_form_number'].widget.attrs['readonly'] = True
    
    context = {
        'form': form,
        'work_order_form_number': Work_order_form.objects.count() + 1
    }
    return render(request, 'web_app/new_work_order_form.html', context)


############################################################################ CLAIMS ############################################################################
@login_required
@permission_required("web_app.view_claim")
def claims(request):
    """show all claims"""
    claims = Claim.objects.order_by('date_added')
    context = {'claims': claims}
    return render(request, 'web_app/claims.html', context)

@login_required
@permission_required("web_app.view_claim")
def newclaim(request):
    """Add a new claim."""
    num_claims = Claim.objects.aggregate(num=Count('claim_number'))['num']
    claim_number = num_claims + 1

    #latest_claim = Claim.objects.last()
    #claim_number = 1 if latest_claim is None else latest_claim.claim_number + 1
    problem_form = inlineformset_factory(Claim, Problem, formset=ProblemForm, fields=('prob_type', 'prob_description', 'prob_part', 'prob_side', 'goodwill'))
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        claim_form = ClaimForm()
        problem_form = problem_form(instance=Claim())

    else:
        # POST data submitted; process data.
        claim_form = ClaimForm(data=request.POST)
        problem_form = problem_form(data=request.POST)
        
        if claim_form.is_valid():
            newclaim = claim_form.save(commit=False)
            newclaim.claim_number = claim_number 
            if request.POST.get('status') == 'Approved':
                newclaim.approved = True
            if request.POST.get('status') == 'Rejected':
                newclaim.rejected = True
            newclaim.save()

            problem_form.instance = newclaim
            problem_form.save()

            # Call the handle_uploaded_files function to save the uploaded images
            files = request.FILES.getlist('claim_images')
            file_paths = handle_uploaded_files(files)

            # Get all existing claims and add the new claim to the queryset
            claimlist = Claim.objects.order_by('date_added')
            claimlist = list(claimlist)
            claimlist.append(newclaim)

            # DEBUGGING
            print(f"New claim {newclaim} saved successfully!")
            print(f"File paths: {file_paths}")

            return redirect('web_app:claims')
        
        # DEBUGGING
        else:
            print(claim_form.errors)

    # Display a blank or invalid form.
    context = {'claim_form': claim_form, 'problem_form': problem_form,'claim_number': claim_number}
    return render(request,'web_app/newclaim.html', context)

# Lookup vehicle information from VIN - currently not working 
@login_required
@permission_required("web_app.view_claim")
def validate_vin(request):
    vin = request.GET.get('vin', '')
    url = f'http://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['Results'][0]
        make = data['Make']
        model = data['Model']
        year = data['ModelYear']
        return JsonResponse({'valid': True, 'make': make, 'model': model, 'year': year})
    else:
        return JsonResponse({'valid': False})

# View Claim
@login_required
@permission_required("web_app.view_claim")
def viewclaim(request, claim_number):
    """Show a single Claim."""
    # Make sure that the Work_order_form object exists in the database
    singleClaim = get_object_or_404(Claim, claim_number=claim_number)

    context = {'viewclaim': singleClaim}
    return render(request, 'web_app/viewclaim.html', context)

# Future Features - Approved and Rejected Claims Lists
@login_required
@permission_required("web_app.view_claim")
def approvedclaims(request):
    """show all approved claims"""
    approvedclaimlist = Claim.objects.filter(status='Approved').order_by('date_added')
    context={'approvedclaims':approvedclaimlist}
    return render(request,'web_app/approvedclaims.html',context)

@login_required
@permission_required("web_app.view_claim")
def rejectedclaims(request):
    """show all rejected claims"""
    approvedclaimlist = Claim.objects.filter(status='Rejected').order_by('date_added')
    context={'rejectedclaims':approvedclaimlist}
    return render(request,'web_app/rejectedclaims.html',context)


############################################################################ REPORTS ############################################################################
@login_required
@permission_required("web_app.view_claim_report")
def reports(request):
    # Process data from claims page and sales page
    claims_data = Claim.objects.all()
    sales_data = Sale.objects.all()

    # Pass data to the template
    context = {
        'claims_data': claims_data,
        'sales_data': sales_data,
    }

    # Render the template
    return render(request, 'web_app/report_dashboard.html', context)

# export sales report as CSV file
@login_required
@permission_required("web_app.view_claim_report")

def export_sales_csv(request):
    sales = Sale.objects.all()

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales-report.csv"'

    # Write the CSV data to the response
    writer = csv.writer(response)
    writer.writerow(['Dealership', 'Daily Sales', 'Total Revenue'])
    for sale in sales:
        writer.writerow([sale.dealership, sale.daily_sales, sale.total_revenue])

    return response

# sales bar graph
@login_required
@permission_required("web_app.view_claim_report")
def export_claims_csv(request):
    claims = Claim.objects.all()

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="claims-report.csv"'

    # Write the CSV data to the response
    writer = csv.writer(response)
    writer.writerow(['Number of Claims'])
    writer.writerow([claims.count()])

    return response
