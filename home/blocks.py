from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


# ============================================
#   HERO BLOCK (Dynamic Landing Section)
# ============================================
class HeroBlock(blocks.StructBlock):
    headline = blocks.CharBlock(required=True, max_length=150, help_text="Main headline for the homepage hero.")
    subheadline = blocks.TextBlock(required=False, help_text="Short supporting description or tagline.")
    background_image = ImageChooserBlock(required=False, help_text="Hero background image.")
    overlay_color = blocks.CharBlock(required=False, help_text="Add overlay color in hex or rgba (e.g. #00000080).")
    button_text = blocks.CharBlock(required=False, max_length=50)
    button_link = blocks.URLBlock(required=False)
    animation_style = blocks.ChoiceBlock(
        choices=[
            ('fade', 'Fade In'),
            ('slide-up', 'Slide Up'),
            ('zoom', 'Zoom In'),
        ],
        default='fade',
        required=False
    )
    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left'),
            ('center', 'Center'),
            ('right', 'Right')
        ],
        default='center',
        required=True
    )

    class Meta:
        template = "blocks/hero.html"
        icon = "image"
        label = "Hero Section"


# ============================================
#   SERVICE OVERVIEW BLOCK (Mini Grid Summary)
# ============================================
class ServiceOverviewItem(blocks.StructBlock):
    icon_class = blocks.CharBlock(
        required=False,
        help_text="FontAwesome or Bootstrap icon class, e.g. 'fa-solid fa-cloud'."
    )
    title = blocks.CharBlock(required=True, max_length=100)
    description = blocks.TextBlock(required=True, max_length=300)
    link_text = blocks.CharBlock(required=False, max_length=50)
    link_url = blocks.URLBlock(required=False)

    class Meta:
        icon = "cog"
        label = "Service Overview Item"
        template = "blocks/service_overview_item.html"


class ServiceOverviewBlock(blocks.StructBlock):
    section_title = blocks.CharBlock(required=True, max_length=120)
    section_description = blocks.TextBlock(required=False)
    services = blocks.ListBlock(ServiceOverviewItem())
    background_color = blocks.CharBlock(
        required=False,
        help_text="Optional background color (e.g. #f5f5f5)."
    )
    columns = blocks.ChoiceBlock(
        choices=[
            ('2', 'Two Columns'),
            ('3', 'Three Columns'),
            ('4', 'Four Columns'),
        ],
        default='3'
    )

    class Meta:
        template = "blocks/service_overview.html"
        icon = "list-ul"
        label = "Service Overview"


# ============================================
#   TESTIMONIAL BLOCK
# ============================================
class TestimonialItem(blocks.StructBlock):
    client_name = blocks.CharBlock(required=True)
    company = blocks.CharBlock(required=False)
    quote = blocks.TextBlock(required=True)
    avatar = ImageChooserBlock(required=False)
    rating = blocks.IntegerBlock(required=False, help_text="Star rating (1–5).")

    class Meta:
        icon = "user"
        label = "Testimonial Item"
        template = "blocks/testimonial_item.html"


class TestimonialSectionBlock(blocks.StructBlock):
    section_title = blocks.CharBlock(required=True, max_length=120)
    testimonials = blocks.ListBlock(TestimonialItem())
    layout_style = blocks.ChoiceBlock(
        choices=[
            ('carousel', 'Carousel'),
            ('grid', 'Grid'),
            ('single', 'Single Highlight')
        ],
        default='carousel'
    )

    class Meta:
        template = "blocks/testimonial_section.html"
        icon = "group"
        label = "Testimonials Section"


# ============================================
#   STATISTICS / METRICS BLOCK
# ============================================
class StatItem(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    value = blocks.CharBlock(required=True)
    icon_class = blocks.CharBlock(required=False)

    class Meta:
        icon = "grip"
        label = "Stat Item"
        template = "blocks/stat_item.html"


class StatsBlock(blocks.StructBlock):
    section_title = blocks.CharBlock(required=False)
    stats = blocks.ListBlock(StatItem())
    theme = blocks.ChoiceBlock(
        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
            ('accent', 'Accent Color'),
        ],
        default='light'
    )

    class Meta:
        template = "blocks/stats.html"
        icon = "bar-chart"
        label = "Company Stats"


# ============================================
#   CALL TO ACTION (CTA) BLOCK
# ============================================
class CTABlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True, max_length=200)
    button_text = blocks.CharBlock(required=True, max_length=50)
    button_link = blocks.URLBlock(required=True)
    style = blocks.ChoiceBlock(
        choices=[
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('dark', 'Dark'),
            ('light', 'Light')
        ],
        default='primary'
    )

    background_image = ImageChooserBlock(required=False)
    overlay_opacity = blocks.DecimalBlock(required=False, max_digits=3, decimal_places=2, help_text="Opacity value (e.g. 0.5)")

    class Meta:
        template = "blocks/cta.html"
        icon = "plus"
        label = "Call to Action"
