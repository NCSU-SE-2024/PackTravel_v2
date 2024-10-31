from django.test import TransactionTestCase
from publish.forms import RideForm

class TestForms(TransactionTestCase):
    def test_rideform_validData(self):

        form = RideForm(data={
                            'source': '1505,Avery Close',
                            'destination' : 'Talley Union',
                            'purpose' : 'Travel',
                            'rideDate' : '10/30/2024',
                            'route' : 'Bus',
                            'routeDetails' : 'Home to College'
                            })
        self.assertTrue(form.is_valid())
    
    def test_rideform_invalidDate(self):

        form = RideForm(data={
                            'source': '1505,Avery Close',
                            'destination' : 'Talley Union',
                            'purpose' : 'Travel',
                            'rideDate' : '13/33/2024',
                            'route' : 'Bus',
                            'routeDetails' : 'Home to College'
                            })
        self.assertFalse(form.is_valid())
        self.assertIn('rideDate', form.errors)
    
    def test_rideform_invalidRoute(self):

        form = RideForm(data={
                            'source': '1505,Avery Close',
                            'destination' : 'Talley Union',
                            'purpose' : 'Travel',
                            'rideDate' : '10/30/2024',
                            'route' : 'Bike',
                            'routeDetails' : 'Home to College'
                            })
        self.assertFalse(form.is_valid())
        self.assertIn('route', form.errors)
    
    def test_rideform_invalidDestination(self):

        form = RideForm(data={
                            'source': '1505,Avery Close',
                            'destination' : '1505,Avery Close',
                            'purpose' : 'Travel',
                            'rideDate' : '10/30/2024',
                            'route' : 'Bike',
                            'routeDetails' : 'Home to College'
                            })
        self.assertFalse(form.is_valid())
        self.assertIn('destination', form.errors)