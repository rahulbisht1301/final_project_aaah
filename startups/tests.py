from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from investors.models import InvestorProfile
from startups.models import Startup, InvestmentApplication


class StartupApplicationTests(TestCase):
    def setUp(self):
        # create a startup user and profile
        self.startup_user = User.objects.create_user(
            username='s1', email='s1@example.com', password='pass', role='STARTUP'
        )
        # signal should create startup automatically but we can ensure
        self.startup = Startup.objects.get(founder=self.startup_user)

        # create two investors
        self.inv1_user = User.objects.create_user(
            username='i1', email='i1@example.com', password='pass', role='INVESTOR'
        )
        self.inv2_user = User.objects.create_user(
            username='i2', email='i2@example.com', password='pass', role='INVESTOR'
        )
        self.inv1 = InvestorProfile.objects.get(user=self.inv1_user)
        self.inv2 = InvestorProfile.objects.get(user=self.inv2_user)

    def test_apply_multiple_investors(self):
        self.client.login(username='s1', password='pass')
        url = reverse('apply_to_investors')
        data = {
            'investor_ids': [str(self.inv1.id), str(self.inv2.id)],
            'subject': 'Funding request',
            'message': 'Please fund us',
            'amount': '50000',
            'equity': '10',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('startup_dashboard'))
        apps = InvestmentApplication.objects.filter(startup=self.startup)
        self.assertEqual(apps.count(), 2)

    def test_apply_single_investor_via_url(self):
        self.client.login(username='s1', password='pass')
        url = reverse('apply_to_investor', args=[self.inv1.id])
        response = self.client.get(url)
        # GET should return 200 and include investor username
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.inv1.user.username)

        response = self.client.post(url, {
            'investor_id': self.inv1.id,
            'subject': 'Seed round',
            'message': 'hi',
            'amount': '1000',
            'equity': '5',
        })
        self.assertRedirects(response, reverse('startup_dashboard'))
        apps = InvestmentApplication.objects.filter(startup=self.startup, investor=self.inv1)
        self.assertEqual(apps.count(), 1)
        self.assertEqual(apps.first().subject, 'Seed round')

    def test_view_application_detail(self):
        self.client.login(username='s1', password='pass')
        app = InvestmentApplication.objects.create(
            startup=self.startup,
            investor=self.inv1,
            subject='Test app',
            message='test',
            amount_requested=1000,
            equity_offered=5
        )
        url = reverse('startup_application_detail', args=[app.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test app')
        self.assertContains(response, self.inv1.user.username)

    def test_delete_application_before_accepted(self):
        self.client.login(username='s1', password='pass')
        app = InvestmentApplication.objects.create(
            startup=self.startup,
            investor=self.inv1,
            subject='To be deleted',
            message='test',
            amount_requested=1000,
            equity_offered=5,
            status='PENDING'
        )
        url = reverse('delete_application', args=[app.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('startup_applications_history'))
        self.assertFalse(InvestmentApplication.objects.filter(id=app.id).exists())

    def test_cannot_delete_accepted_application(self):
        self.client.login(username='s1', password='pass')
        app = InvestmentApplication.objects.create(
            startup=self.startup,
            investor=self.inv1,
            subject='Accepted app',
            message='test',
            amount_requested=1000,
            equity_offered=5,
            status='ACCEPTED'
        )
        url = reverse('delete_application', args=[app.id])
        response = self.client.post(url)
        # should redirect back to detail page, not delete
        self.assertTrue(InvestmentApplication.objects.filter(id=app.id).exists())

    def test_cannot_delete_rejected_application(self):
        self.client.login(username='s1', password='pass')
        app = InvestmentApplication.objects.create(
            startup=self.startup,
            investor=self.inv1,
            subject='Rejected app',
            message='test',
            amount_requested=1000,
            equity_offered=5,
            status='REJECTED'
        )
        url = reverse('delete_application', args=[app.id])
        response = self.client.post(url)
        # should not delete rejected applications
        self.assertTrue(InvestmentApplication.objects.filter(id=app.id).exists())
