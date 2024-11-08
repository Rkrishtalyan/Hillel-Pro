from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime


# ---- View Functions ----

def home(request):
    """
    Render the home page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: The rendered home page.
    :rtype: HttpResponse
    """
    return render(request, 'main/home.html')


def about(request):
    """
    Render the about page with company information.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: The rendered about page with context data.
    :rtype: HttpResponse
    """
    context = {
        'company_description': (
            "The Dark Brotherhood of Skyrim is a clandestine society dedicated to empowering students "
            "through specialized academic support inspired by the enigmatic world of Skyrim. "
            "Drawing parallels from the stealth and precision of the Dark Brotherhood, "
            "we offer a unique approach to learning that emphasizes strategic thinking, dedication, and excellence.\n\n"
            "Founded by scholars and enthusiasts of the Elder Scrolls universe, "
            "our mission is to blend fantasy-inspired methodologies with real-world academic assistance. "
            "Whether you're navigating complex assignments or seeking to deepen your understanding of mythical lore, "
            "our brotherhood stands ready to guide you."
        ),
        'last_updated': datetime.now(),
    }
    return render(request, 'main/about.html', context)


# ---- Class-Based Views ----

class ContactView(TemplateView):
    """
    Represent the contact page with contact details for the Dark Brotherhood.

    :var template_name: The template used for the contact page.
    :type template_name: str
    """
    template_name = 'main/contact.html'

    def get_context_data(self, **kwargs):
        """
        Get context data for the contact page, including contact details.

        :param kwargs: Additional context keyword arguments.
        :type kwargs: dict
        :return: The context with contact details.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context['email'] = 'shadowbrotherhood@skyrim.com'
        context['phone'] = '+1-800-SKYRIM'
        context['address'] = '123 Shadow Lane, Whiterun, Tamriel'
        context['has_contact_data'] = True  # Set to False to test the 'default' filter
        return context


class ServiceView(TemplateView):
    """
    Represent the service page, listing available services of the Dark Brotherhood.

    :var template_name: The template used for the service page.
    :type template_name: str
    """
    template_name = 'main/service.html'

    def get_services(self):
        """
        Define and return a list of services offered by the Dark Brotherhood.

        :return: List of service details.
        :rtype: list of dict
        """
        services = [
            {
                'name': 'Stealth Tutoring',
                'description': (
                    'Personalized tutoring sessions in various subjects, '
                    'ensuring you master your coursework with precision and efficiency.'
                ),
                'available': True,
                'category': 'Assistance',
            },
            {
                'name': 'Lore Workshops',
                'description': (
                    'Dive deep into the rich narratives of Skyrim and beyond, '
                    'enhancing your creative writing and analytical skills.'
                ),
                'available': True,
                'category': 'Workshops',
            },
            {
                'name': 'Assignment Assassins',
                'description': (
                    'Expert assistance with homework and projects, '
                    'delivered with the stealth and accuracy of a master assassin.'
                ),
                'available': False,
                'category': 'Assistance',
            },
            {
                'name': 'Study Camps',
                'description': (
                    'Intensive study sessions and workshops to prepare you for exams '
                    'and academic challenges, inspired by the rigorous training of the Dark Brotherhood.'
                ),
                'available': True,
                'category': 'Camps',
            },
            {
                'name': 'Resource Library',
                'description': (
                    'Access a vast collection of study materials, guides, '
                    'and reference texts curated to support your educational journey.'
                ),
                'available': True,
                'category': 'Resources',
            },
        ]
        return services

    def get_context_data(self, **kwargs):
        """
        Get context data for the service page, including filtered service list.

        Filters services based on search query and category specified in GET parameters.

        :param kwargs: Additional context keyword arguments.
        :type kwargs: dict
        :return: The context with service details and filters applied.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        services = self.get_services()

        # Filter services based on search query and category
        query = self.request.GET.get('q', '').lower()
        category = self.request.GET.get('category', '')

        if query or category:
            filtered_services = []
            for service in services:
                match_query = True
                match_category = True

                # Check for query match
                if query:
                    match_query = query in service['name'].lower() or query in service['description'].lower()

                # Check for category match
                if category:
                    match_category = service['category'] == category

                # Include service if it matches both query and category
                if match_query and match_category:
                    filtered_services.append(service)

            context['services'] = filtered_services
        else:
            context['services'] = services

        context['categories'] = sorted(set(service['category'] for service in services))
        context['query'] = self.request.GET.get('q', '')
        context['selected_category'] = category
        context['last_updated'] = datetime.now()
        return context
