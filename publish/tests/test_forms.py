from django.test import TransactionTestCase
from publish.forms import RideForm

class TestForms(TransactionTestCase):
    def test_rideform_validData(self):

        form = RideForm(data={
                            'source': '1505,Avery Close',
                            'destination' : 'Talley Union',
                            'purpose' : 'Travel',
                            'rideDate' : '2024-11-15',
                            'route' : 'Bus',
                            'routeDetails' : 'Home to College'
                            })
        self.assertTrue(form.is_valid())
    
    def test_rideform_invalidDate(self):

        form = RideForm(data={
                            'source': '1505,Avery Close',
                            'destination' : 'Talley Union',
                            'purpose' : 'Travel',
                            'rideDate' : '2024-04-12',
                            'route' : 'Bus',
                            'routeDetails' : 'Home to College'
                            })
        self.assertFalse(form.is_valid())
        self.assertIn('rideDate', form.errors)
    
    def test_rideform_pastDate(self):

        form = RideForm(data={
                            'source': '1505,Avery Close',
                            'destination' : 'Talley Union',
                            'purpose' : 'Travel',
                            'rideDate' : '2024-10-11',
                            'route' : 'Bus',
                            'routeDetails' : 'Home to College'
                            })
        self.assertFalse(form.is_valid())
        self.assertIn('rideDate', form.errors)
    
    def test_rideform_futureDate(self):

        form = RideForm(data={
                            'source': '1505,Avery Close',
                            'destination' : 'Talley Union',
                            'purpose' : 'Travel',
                            'rideDate' : '2025-10-11',
                            'route' : 'Bus',
                            'routeDetails' : 'Home to College'
                            })
        self.assertFalse(form.is_valid())
        self.assertIn('rideDate', form.errors)
    
    def test_rideform_invalidDestination(self):

        form = RideForm(data={
                            'source': '1505,Avery Close',
                            'destination' : '1505,Avery Close',
                            'purpose' : 'Travel',
                            'rideDate' : '2024-11-15',
                            'route' : 'Bike',
                            'routeDetails' : 'Home to College'
                            })
        self.assertFalse(form.is_valid())
        self.assertIn('Source and destination must be different.', form.errors['__all__'])