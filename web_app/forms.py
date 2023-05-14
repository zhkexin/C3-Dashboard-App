from django import forms
from .models import Claim, Problem, Work_order_form 
from django.forms import inlineformset_factory

############################################################################ SALES ############################################################################

class Work_order_form_form(forms.ModelForm):
    work_order_form_number = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Work_order_form
        fields = ['work_order_form_number','product', 'quantity_used', 'payment_amount', 'customer_name', 'customer_phone', 'vehicle_make', 'vehicle_vin', 'dealership_name', 'dealership_phone', 'contact_name', 'dealership_email', 'address', 'country', 'province', 'postal_code']
        labels = {'dealership_name': 'Dealership Name', 'product': 'Product Name', 'customer_name': 'Customer Name', 'customer_phone': 'Customer Phone', 'vehicle_make': 'Vehicle Make', 'vehicle_vin': 'Vehicle VIN', 'dealership_phone': 'Dealership Phone', 'contact_name': 'Contact Name', 'dealership_email': 'Dealership Email', 'postal_code': 'Postal Code'}
        
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['work_order_form_number'].widget.attrs['readonly'] = True  


############################################################################ CLAIMS ############################################################################

class ClaimForm(forms.ModelForm):
    claim_date = forms.DateTimeField(input_formats=['%B %d, %Y'])
    problem_formset = inlineformset_factory(Claim, Problem, fields=('prob_type', 'prob_description', 'prob_part', 'prob_side', 'goodwill'))

    class Meta:
        model = Claim
        fields = '__all__' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['claim_approvedby'].required = False
        self.fields['claim_approvedto'].required = False
        self.fields['claim_approved_date'].required = False
        self.fields['claim_rejectedby'].required = False
        self.fields['claim_rejection_date'].required = False
        self.fields['claim_rejection_reason'].required = False

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')

        if status == 'Approved':
            if not cleaned_data.get('claim_approvedby'):
                self.add_error('claim_approvedby', 'This field is required.')
            if not cleaned_data.get('claim_approvedto'):
                self.add_error('claim_approvedto', 'This field is required.')
            if not cleaned_data.get('claim_approved_date'):
                self.add_error('claim_approved_date', 'This field is required.')
        
        if status == 'Rejected':
            if not cleaned_data.get('claim_rejectedby'):
                self.add_error('claim_rejectedby', 'This field is required.')
            if not cleaned_data.get('claim_rejection_date'):
                self.add_error('claim_rejection_date', 'This field is required.')
            if not cleaned_data.get('claim_rejection_reason'):
                self.add_error('claim_rejection_reason', 'This field is required.')

        return cleaned_data
  
class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('prob_type', 'prob_description', 'prob_part', 'prob_side', 'goodwill')
        exclude = ('prob_id',)


