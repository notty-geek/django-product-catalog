from behave import given, then, when
from playwright.sync_api import expect


@given("I open the product catalog")
def open_catalog(context):
    context.page.goto(context.catalog_url)


@when('I enter "{text}" in the description search')
def enter_description(context, text):
    context.page.get_by_role("textbox", name="Search descriptions").fill(text)


@when('I choose the "{category}" category')
def choose_category(context, category):
    context.page.get_by_role("combobox", name="Category").select_option(label=category)


@when('I select the "{tag}" tag')
def select_tag(context, tag):
    context.page.get_by_role("checkbox", name=tag, exact=True).check()


@when("I apply the filters")
def apply_filters(context):
    context.page.get_by_role("button", name="Apply filters").click()


@then("I see exactly these products")
def check_products(context):
    results = context.page.get_by_role("region", name="Products")
    names = results.get_by_role("heading", level=3)
    expect(names).to_have_text([row["Product"] for row in context.table])
