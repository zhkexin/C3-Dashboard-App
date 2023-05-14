from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


############################################################################ SALES ############################################################################
# Work Orders
class Work_order_form(models.Model):

    # A specific Work Order Form
    #Id field work_order_form_number
    work_order_form_number = models.AutoField(primary_key=True)
    
    date_added = models.DateTimeField(auto_now_add=True) 
    
    product = models.CharField(max_length=200, default='Rust Protection')     #the product that is being sold EX: rust protection, VIN etching
    quantity_used = models.CharField(max_length=200, default=1) 
    payment_amount = models.CharField(max_length=200, default=100) 
    
    customer_name = models.CharField(max_length=200, default='Bob') 
    customer_phone = models.CharField(max_length=200, default='7801234567') 
    vehicle_make = models.CharField(max_length=200, default='Honda') 
    vehicle_vin = models.CharField(max_length=200, default='11111') 
    
    
    
    dealership_name = models.CharField(max_length=200, default = 'Toyota')
    dealership_phone = models.CharField(max_length=200, default = '7801234567')
    contact_name = models.CharField(max_length=200, default='Bob') 
    dealership_email = models.CharField(max_length=200, default = 'dealership@gmail.com')
    address = models.CharField(max_length=200, default = '47 Wallabeye Way') 
    country = models.CharField(max_length=200, default = 'Canada') 
    province = models.CharField(max_length=200, default = 'Alberta') 
    postal_code = models.CharField(max_length=200, default = 'T8V T9C') 
    text = models.CharField(max_length=200)
    

    def __str__(self):
        # Return a string representation of the model
        return f"Work Order Form {self.work_order_form_number}"


############################################################################ CLAIMS ############################################################################

# Claim Model
class Claim(models.Model):
    # Claim Information
    claim_number = models.AutoField(primary_key=True, default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('status_info', 'Information Only'),
        ('status_pending', 'Pending'),
        ('status_submitted', 'Submitted'),
        ('status_approved', 'Approved'),
        ('status_rejected', 'Rejected'),
        ('status_paid', 'Paid'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Information Only')

    claim_date = models.DateTimeField(blank=True, default=timezone.now) 
    effective_date = models.DateTimeField(blank=True, default=timezone.now) 
    process_date = models.DateTimeField(blank=True, default=timezone.now) 

    po_num = models.CharField(max_length=200, default='N/A')
    file_num = models.CharField(max_length=200, default='N/A')
    agreement = models.CharField(max_length=200, default='N/A')

    # Aprroval Information
    claim_approvedby = models.CharField(max_length=50, blank=True)
    claim_approvedto = models.CharField(max_length=50, blank=True)
    claim_approved_date = models.DateTimeField(blank=True, null=True, default='') 

    # Rejected Information
    claim_rejectedby = models.CharField(max_length=50, blank=True)
    claim_rejection_date = models.DateTimeField(blank=True, null=True, default='') 
    claim_rejection_reason = models.CharField(max_length=1000, blank=True)

    # Repair Shop Information
    shop_active = models.BooleanField(default=False)
    shop_name = models.CharField(max_length=200, default='N/A')
    shop_phone = models.CharField(max_length=12, default='123-456-7890')
    shop_contact = models.CharField(max_length=200, blank=True)
    shop_email = models.EmailField(blank=True)
    shop_address = models.CharField(max_length=200, default='1234 Main St')
    shop_address2 = models.CharField(max_length=200, blank=True)

    COUNTRY_CHOICES = [
        ('CAN', 'Canada'),
    ]
    shop_country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='CAN')
   
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('BC', 'British Columbia'),
        ('MB', 'Manitoba'),
        ('NB', 'New Brunswick'),
        ('NL', 'Newfoundland and Labrador'),
        ('NT', 'Northwest Territories'),
        ('NS', 'Nova Scotia'),
        ('NU', 'Nunavut'),
        ('ON', 'Ontario'),
        ('PE', 'Prince Edward Island'),
        ('QC', 'Quebec'),
        ('SK', 'Saskatchewan'),
        ('YT', 'Yukon'),
    ]
    shop_province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, default='Ontario')

    shop_postalcode = models.CharField(max_length=7, default='A1A 1A1')

    # Customer Information
    cust_fname = models.CharField(max_length=30, default='N/A')
    cust_lname = models.CharField(max_length=30, default='N/A')

    policy_type = models.CharField(max_length=50, default='N/A')
    coverage_type = models.CharField(max_length=50, default='N/A')
    vin = models.CharField(max_length=30, default='JTHBP262495004947')

    # Claim Details
    claim_details = models.CharField(max_length=1000, blank=True)

    # Estimate Information
    claim_estimate1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    claim_estimate2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    claim_req_amt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    est_tier2 = models.BooleanField(default=False)

    claim_estimate3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    claim_estimate4 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    claim_estimate5 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    # Amount Information
    claim_amt_agreed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    claim_deductible = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    claim_net_amt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    
    # Payment Information
    cheque_num = models.CharField(max_length=50, blank=True)
    cheque_pay_to = models.CharField(max_length=50, blank=True)
    cheque_date = models.DateTimeField(blank=True, null=False, default='') 
    cheque_amt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Convert empty strings to None before saving
        if not self.claim_estimate1:
            self.claim_estimate1 = 0.00
        if not self.claim_estimate2:
            self.claim_estimate2 = 0.00
        if not self.claim_estimate3:
            self.claim_estimate3 = 0.00
        if not self.claim_estimate4:
            self.claim_estimate4 = 0.00
        if not self.claim_estimate5:
            self.claim_estimate5 = 0.00
        if not self.claim_net_amt:
            self.claim_net_amt = 0.00
        if not self.cheque_amt:
            self.cheque_amt = 0.00
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Claim {self.claim_number}"
    
# Claim Problem Model
class Problem(models.Model):
    prob_id = models.AutoField(primary_key=True)
    claim_number = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='problems')

    # Problem Information
    PROBLEM_TYPE_CHOICES = [
        ('prob_fabric', 'Fabirc'),
        ('prob_leathvin', 'Leather/Vinyl'),
        ('prob_paint', 'Paint'),
        ('prob_rust', 'Rust'),
        ('prob_theft', 'Theft'),
        ('prob_undercoat', 'Undercoat'),
    ]
    prob_type = models.CharField(max_length=30, choices=PROBLEM_TYPE_CHOICES, default='Fabric')

    prob_description = models.TextField(default='N/A')
    prob_part = models.CharField(max_length=50, default='N/A')

    PROBLEM_SIDE_CHOICES = [
        ('prob_bothsides', 'Both'),
        ('prob_leftside', 'Left'),
        ('prob_rightside', 'Right'),
        ('prob_noside', 'N/A'),
    ]
    prob_side = models.CharField(max_length=30, choices=PROBLEM_SIDE_CHOICES, default='N/A')

    goodwill = models.DecimalField(max_digits=7, decimal_places=2, null=True, default=0.00)

    def __str__(self):
        return f"Problem {self.prob_id}"


############################################################################ REPORTS ############################################################################

# Sale Model for Reports
class Sale(models.Model):
    car_dealership = models.CharField(max_length=100)
    daily_sales = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

# Claim Model for Reports
class ClaimReport(models.Model):
    number_of_claims = models.IntegerField()