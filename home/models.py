from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from modelcluster.fields import ParentalKey

from . import blocks as home_blocks

class HomePage(Page):

    tagline = models.CharField(
        max_length=255,
        blank=True,
        help_text="The tagline for the homepage"
    )

    body = StreamField([
        ('hero', home_blocks.HeroBlock()),
        ('services_overview', home_blocks.ServiceOverviewBlock()),
        ('testimonial_section', home_blocks.TestimonialSectionBlock()),
        ('stats', home_blocks.StatsBlock()),
        ('cta', home_blocks.CTABlock()),
    ], use_json_field=True, blank=True)

    meta_description =models.TextField(
        max_length=3000,
        blank=True,
        help_text="The meta description for the homepage"
    )

    show_in_navigation = models.BooleanField(
        default=True,
        help_text="Check to show this page in the navigation"
    )

    footer_note = models.CharField(
        max_length=255,
        blank=True,
        help_text="The footer note for the homepage"
    )

    content_panels = Page.content_panels + [
        FieldPanel('tagline'),
        FieldPanel('body'),
    ]

    settings_panels = Page.settings_panels + [
        MultiFieldPanel([
            FieldPanel('meta_description'),
            FieldPanel('show_in_navigation'),
            FieldPanel('footer_note'),
        ], heading="Homepage Settings")
    ]

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
    
    def get_context(self, request):
        context = super().get_context(request)
        context['company_name'] = "VirtuSys Global"
        context['seo_description'] = self.meta_description or "Empowering global businesses through IT innovation."
        context['api_data'] = HomeAPIResponse.get_data()
        return context
class HeroSlide(Orderable):

    page = ParentalKey(HomePage, related_name='hero_slides')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    button_text = models.CharField(max_length=255, blank=True)
    button_link = models.URLField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('subtitle'),
        FieldPanel('image'),
        FieldPanel('button_text'),
        FieldPanel('button_link'),
    ]

    class Meta:
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"
    
    def __str__(self):
        return f"{self.title}"

@register_setting
class GlobalSiteSettings(BaseSiteSetting):
    site_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    company_email = models.EmailField(blank=True)
    company_phone = models.CharField(max_length=20, blank=True)
    company_address = models.CharField(max_length=255, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    theme_color = models.CharField(max_length=20, blank=True, help_text="The theme color for the site")

    panels = [
        MultiFieldPanel([
            FieldPanel('site_logo'),
            FieldPanel('company_email'),
            FieldPanel('company_phone'),
            FieldPanel('company_address'),
        ], heading="Company Info"),
        MultiFieldPanel([
            FieldPanel('linkedin_url'),
            FieldPanel('twitter_url'),
            FieldPanel('facebook_url'),
        ], heading="Design and Rebranding")
    ]

    class Meta:
        verbose_name = "Global Site Settings"
        verbose_name_plural = "Global Site Settings"
    
    def __str__(self):
        return "Global Site Settings"

class HomeAPIResponse(models.Model):
    @staticmethod
    def get_data():
        return {
            "company": "VirtuSys Global",
            "overview": "Empowering global businesses through IT innovation.",
            "services": [
                {
                    "title": "Cloud Infrastructure",
                    "description": "Scalable, secure cloud migration and optimization services."
                },
                {
                    "title": "AI & Automation",
                    "description": "Intelligent process automation for enterprise growth."
                },
                {
                    "title": "Cybersecurity",
                    "description": "Advanced, proactive defense systems for digital resilience."
                }
            ],
            "contact": {
                "email": "info@virtusysglobal.com",
                "phone": "+1 (800) 555-0199",
                "address": "500 Park Avenue, New York, NY, USA"
            }
        }