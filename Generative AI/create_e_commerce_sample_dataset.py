# Databricks notebook source
print("Creating sample data table.")

# COMMAND ----------

# You do not need to run this notebook by itself. It is run in the Initial Setup notebook.
from pyspark.sql.types import *
from pyspark.sql.functions import udf, col
import random
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, DecimalType
import pandas as pd
import random
import string
from datetime import datetime, timedelta
from decimal import Decimal
import re


num_rows = 200

def random_date(start_date="2020-01-01", end_date="2024-12-01"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    random_days = random.randrange(delta.days)
    random_seconds = random.randrange(86400)
    return start + timedelta(days=random_days, seconds=random_seconds)

product_keywords = [
    "Wireless", "Bluetooth", "Smart", "Portable", "UltraSlim",
    "Rechargeable", "4K", "Noise Cancelling", "Ergonomic", "Stainless Steel",
    "Foldable", "Adjustable", "High Precision", "Touchscreen", "LED",
]

product_items = [
    "Headphones", "Speaker", "Air Purifier", "Keyboard", "Mouse",
    "Coffee Maker", "Fitness Tracker", "Power Bank", "Smart Lamp",
    "Water Bottle", "Laptop Stand", "Travel Bag", "Microphone",
    "Webcam", "Projector", "Juicer", "Hair Dryer"
]

def random_title():
    return f"{random.choice(product_keywords)} {random.choice(product_items)}"

data = []
for _ in range(num_rows):
    row = {
        "Timestamp": random_date(),
        "Title": random_title()
    }
    data.append(row)

pdf = pd.DataFrame(data)
df_products = spark.createDataFrame(pdf)



brand_prefixes = [
    "Nova", "Prime", "Aero", "Luma", "Vertex", "Pixel", "Urban",
    "Zenith", "Echo", "Nimbus", "Fusion", "Astra", "Quantum",
    "Vista", "Polar", "Terra"
]

brand_suffixes = [
    "Tech", "Labs", "Works", "Gear", "House", "Studio",
    "Core", "Wave", "Systems", "Designs", "Essentials",
    "Line", "World", "Hub", "Select"
]

@udf(StringType())
def gen_brand():
    return random.choice(brand_prefixes) + random.choice(brand_suffixes)

long_description_templates = [
    (
        "{title} from {brand} is intended as a practical option for people who want something reliable "
        "without adding unnecessary complexity to their daily routine. It focuses on straightforward operation, "
        "so you do not need any special experience to start using it, and it fits easily into a variety of home "
        "or office setups. The overall build aims to balance durability with a clean, neutral appearance, making "
        "it suitable for different styles of spaces. In regular use, the goal is to keep adjustments simple and "
        "predictable, so that you can focus on your actual work or activities rather than managing the product "
        "itself. It is designed to handle everyday tasks at a steady pace instead of chasing extreme performance "
        "or very specific niche use cases. With that approach, {title} can act as a quiet helper in the background, "
        "supporting routine tasks in a consistent way. Key aspects include {features}, combined to offer a balanced "
        "experience that feels easy to live with over time."
    ),
    (
        "{brand} created the {title} for users who prefer dependable tools that stay out of the way and simply do "
        "their job. Rather than focusing on flashy add-ons, the product emphasizes a clear layout and familiar "
        "controls, so it feels approachable even on the first use. It is meant to sit comfortably in shared spaces, "
        "whether that is a study corner, a living room, or a small office. The materials and structure are selected "
        "to support regular use, with the intention that you do not have to worry about constant fine-tuning or "
        "adjustment. Over time, the aim is for the {title} to blend into your routine, becoming one of those items "
        "you simply rely on without thinking too much about it. Core design points include {features}, which are "
        "grouped together to prioritize ease of use, steady performance, and a calm, unobtrusive presence in day-to-day life."
    ),
    (
        "The {title} offered by {brand} is shaped around the idea that a useful product does not need to be complicated "
        "to be effective. It is meant for people who want something they can set up once and then trust during regular "
        "work or home activities. The form factor is kept modest so that it can fit on a desk, shelf, or counter without "
        "demanding extra space or attention. During typical use, it aims to provide consistent behavior, so you can focus "
        "on your tasks and not on the tool itself. Rather than specializing in a narrow scenario, it is built to handle a "
        "range of everyday situations at a steady level of quality. Features such as {features} are included to support "
        "this general-purpose approach, offering a mix of practicality, familiarity, and low-effort upkeep. The result is "
        "a product that is intended to quietly support your routine instead of becoming another source of complexity."
    ),
    (
        "{brand}'s {title} is designed around everyday patterns of use, where reliability and clarity matter more than "
        "constant adjustment. The intent is to provide something that feels straightforward from the moment you take it "
        "out of the box, with controls and behavior that are easy to understand. Its visual style is kept neutral so that "
        "it can blend into different environments without looking out of place. Over time, it is meant to remain stable, "
        "so that you do not have to continuously relearn how to interact with it. Instead of chasing short-lived trends, "
        "the design focuses on steady function and predictable responses. The inclusion of {features} is aimed at supporting "
        "daily tasks while keeping the overall experience calm and manageable. In this way, the {title} is positioned as a "
        "supportive background tool, helping you maintain momentum in your routine without demanding extra attention."
    ),
    (
        "With the {title}, {brand} aims to offer a practical companion for routine tasks, whether you are at home or at work. "
        "The product is structured so that you can start using it with minimal preparation, and its proportions are chosen to "
        "fit comfortably into compact spaces. The interaction model is intentionally straightforward, reducing the need to "
        "consult detailed instructions once you have become familiar with it. During extended use, the goal is to keep things "
        "steady rather than surprising, allowing you to build habits around how it behaves. This makes it suitable for people "
        "who value calm, predictable tools over highly specialized equipment. The set of characteristics grouped under "
        "{features} reflects this philosophy, focusing on ease of handling, simple upkeep, and consistent performance. Taken "
        "together, these aspects are meant to create a balanced experience that supports your regular activities without "
        "drawing unnecessary attention to itself."
    ),
]

@udf(StringType())
def gen_long_description(title, brand, features):
    t = title if title else "This product"
    b = brand if brand else "the manufacturer"
    f = features if features else "practical design; simple operation; suitable for everyday use"

    template = random.choice(long_description_templates)
    paragraph = template.format(title=t, brand=b, features=f)
    return paragraph



@udf(StringType())
def gen_initial_price():
    price = round(random.uniform(10, 999), 2)
    return f"{price:.2f}"

@udf(DecimalType(38,0))
def fix_final_price(initial_price, discount_str):
    try:
        base = float(initial_price)
    except:
        base = random.uniform(10, 999)
    if discount_str is None:
        discount_percent = random.randint(5, 30)
    else:
        match = re.search(r"(\d+)", discount_str)
        if match:
            discount_percent = int(match.group(1))
        else:
            discount_percent = 0
    final_price_val = base * (1 - (discount_percent / 100.0))
    final_price_int = int(max(1, round(final_price_val)))
    return Decimal(str(final_price_int))

currencies = ["USD", "INR", "EUR", "GBP", "CAD", "AUD"]

@udf(StringType())
def gen_currency():
    return random.choice(currencies)

availability_options = [
    "In Stock",
    "Limited Stock",
    "Out of Stock",
    "Available Soon",
    "Preorder Available"
]

@udf(StringType())
def gen_availability():
    return random.choice(availability_options)



@udf(DecimalType(38,0))
def gen_reviews_count():
    return Decimal(str(random.randint(0, 50000)))

@udf(DecimalType(38,0))
def gen_number_of_sellers():
    return Decimal(str(random.randint(2, 10)))

category_options = [
    "Electronics > Audio > Headphones",
    "Electronics > Computers > Accessories",
    "Electronics > Home Audio > Speakers",
    "Home & Kitchen > Small Appliances > Coffee Makers",
    "Home & Kitchen > Storage & Organization",
    "Home & Kitchen > Lighting > Table Lamps",
    "Sports & Outdoors > Fitness > Accessories",
    "Sports & Outdoors > Camping & Hiking > Gear",
    "Beauty & Personal Care > Hair Care > Styling",
    "Beauty & Personal Care > Skin Care > Tools",
    "Office Products > Office Electronics > Printers",
    "Office Products > Furniture > Chairs",
    "Automotive > Interior Accessories",
    "Toys & Games > Learning & Education",
    "Toys & Games > Puzzles",
    "Industrial & Scientific > Test & Measurement"
]

@udf(StringType())
def gen_categories():
    return random.choice(category_options)

def make_fake_asin():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=10))

@udf(StringType())
def gen_asin():
    return make_fake_asin()

root_categories = [
    "Electronics",
    "Home & Kitchen",
    "Computers & Accessories",
    "Sports & Outdoors",
    "Beauty & Personal Care",
    "Toys & Games",
    "Automotive",
    "Office Products",
    "Industrial & Scientific"
]

@udf(StringType())
def gen_root_bs_rank():
    rank = random.randint(1, 500000)
    root_cat = random.choice(root_categories)
    return f"#{rank} in {root_cat}"


from pyspark.sql.types import StringType, DecimalType
from pyspark.sql.functions import udf, col
import random
import string

fake_domains = [
    "shoplite.store", "megabuyhub.com", "trendifyonline.net",
    "primegoodsmart.co", "dealstreak.io", "retailnova.com",
    "quickmartdirect.org", "brightcart.net", "hyperretail.co",
    "urbangoods.shop"
]

@udf(StringType())
def gen_domain():
    return random.choice(fake_domains)

def random_slug():
    words = ["portable", "wireless", "smart", "premium", "classic",
             "ultra", "modern", "compact", "sleek", "advance", "eco"]
    nouns = ["device", "item", "product", "gear", "accessory", "unit"]
    return f"{random.choice(words)}-{random.choice(nouns)}-{random.randint(1000,9999)}"

@udf(StringType())
def gen_url(domain):
    return f"https://{domain}/product/{random_slug()}/"

@udf(StringType())
def gen_image_url(domain):
    img_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"https://cdn.{domain}/images/{img_id}.jpg"

weights = ["250g", "500g", "750g", "1kg", "1.2kg", "1.5kg", "2kg", "2.5kg", "3kg"]

@udf(StringType())
def gen_item_weight():
    return random.choice(weights)

delivery_options = [
    "Delivered within 3–5 business days",
    "Delivered within 5–7 business days",
    "Expected delivery: 2–4 days",
    "Ships within 48 hours",
    "Arrives next week",
    "Delivery estimate: 6–10 days",
    "Fast delivery available",
    "Standard delivery only"
]

@udf(StringType())
def gen_delivery():
    return random.choice(delivery_options)

@udf(DecimalType(38,1))
def gen_rating():
    half_steps = random.randint(2, 10)
    value = half_steps / 2.0
    return Decimal(f"{value:.1f}")

from pyspark.sql.types import StringType
from pyspark.sql.functions import udf, col
import random
from datetime import datetime, timedelta
import string

@udf(StringType())
def gen_product_dimensions():
    length = random.randint(5, 50)
    width = random.randint(3, 30)
    height = random.randint(1, 25)
    return f"{length} x {width} x {height} cm"

def random_date_str(start_date="2018-01-01", end_date="2024-12-01"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    random_days = random.randrange(delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

@udf(StringType())
def gen_date_first_available():
    return random_date_str()

discount_options = [
    "No discount",
    "5% off",
    "10% off",
    "12% off",
    "15% off",
    "20% off",
    "25% off",
    "30% off",
    "Limited-time 18% off"
]

@udf(StringType())
def gen_discount():
    return random.choice(discount_options)

feature_templates = [
    "Lightweight design; Easy to clean; Suitable for daily use",
    "Compact form factor; Simple controls; Works well in home or office",
    "Durable build; Stable performance; Low maintenance",
    "Quick setup; Clear instructions; Designed for everyday tasks",
    "Adjustable settings; Quiet operation; Space-saving design",
    "Energy-conscious operation; Reliable components; Minimal setup",
    "Portable size; User-friendly layout; Supports regular use",
    "Sturdy construction; Balanced design; Straightforward handling",
    "Smooth operation; Neutral finish; Blends into most spaces",
    "Non-slip base; Practical layout; Optimized for regular workloads"
]

@udf(StringType())
def gen_features():
    return random.choice(feature_templates)

def random_model_code():
    prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
    digits = random.randint(100, 999)
    suffix = random.choice(string.ascii_uppercase)
    return f"{prefix}-{digits}{suffix}"

@udf(StringType())
def gen_model_number():
    return random_model_code()

manufacturer_names = [
    "LumaTek Industries",
    "Vertex Global Manufacturing",
    "AeroCore Appliances",
    "NovaLine Electronics",
    "PolarEdge Systems",
    "TerraCraft Labs",
    "FusionPoint Devices",
    "EchoStone Technologies",
    "Zenora Home Products",
    "BrightWave Solutions",
    "UrbanAxis Hardware",
    "NimbusPeak Innovations"
]

@udf(StringType())
def gen_manufacturer():
    return random.choice(manufacturer_names)

df_products = (
    df_products
        .withColumn("Brand", gen_brand())
        .withColumn("Initial_Price", gen_initial_price())
        .withColumn("Currency", gen_currency())
        .withColumn("Availability", gen_availability())
        .withColumn("Review_Count", gen_reviews_count())
        .withColumn("Categories", gen_categories())
        .withColumn("ASIN", gen_asin())
        .withColumn("Number_of_Sellers", gen_number_of_sellers())
        .withColumn("Root_BS_Rank", gen_root_bs_rank())
        .withColumn("Domain", gen_domain())
        .withColumn("URL", gen_url(col("Domain")))
        .withColumn("Image_URL", gen_image_url(col("Domain")))
        .withColumn("Item_Weight", gen_item_weight())
        .withColumn("Delivery", gen_delivery())
        .withColumn("Rating", gen_rating())
        .withColumn("Product_Dimensions", gen_product_dimensions())
        .withColumn("Date_First_Available", gen_date_first_available())
        .withColumn("Discount", gen_discount())
        .withColumn("Final_Price", fix_final_price(col("Initial_Price"), col("Discount")))
        .withColumn("Features", gen_features())
        .withColumn("Description", gen_long_description(col("Title"), col("Brand"), col("Features")))
        .withColumn("Model_Number", gen_model_number())
        .withColumn("Manufacturer", gen_manufacturer())
)
final_cols = [
    "Timestamp",
    "Title",
    "Brand",
    "Description",
    "Initial_Price",
    "Final_Price",
    "Currency",
    "Availability",
    "Review_Count",
    "Categories",
    "ASIN",
    "Number_of_Sellers",
    "Root_BS_Rank",
    "Domain",
    "URL",
    "Image_URL",
    "Item_Weight",
    "Delivery",
    "Rating",
    "Product_Dimensions",
    "Date_First_Available",
    "Discount",
    "Features",
    "Model_Number",
    "Manufacturer"
]
df = df_products.select(*final_cols)

df.write.mode("overwrite").saveAsTable(
    f"{catalog_name}.{schema_name}.e_commerce_product_listings_dataset"
)
print("Done.")

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>