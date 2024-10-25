from django.test import TransactionTestCase
from publish.forms import RideForm

class TestForms(TransactionTestCase):
    def test_rideform_validData(self):

        form = RideForm(data={
                            'source': '',
                            'destination' : '',
                            'purpose' : '',
                            'rideDate' : '',
                            'route' : '',
                            'routeDetails' : ''
                            })
        self.assertFalse(form.is_valid())