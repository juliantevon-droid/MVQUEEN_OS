# Activate your project folder
cd /storage/emulated/0/mvqueen_engine

# Run metafield definitions
python3 - << 'EOF'
from mvqueen_engine.shopify.metafield_definitions import MetafieldDefinitionCreator

creator = MetafieldDefinitionCreator(
    shop_url="YOURSHOP.myshopify.com",
    access_token="YOUR_ADMIN_API_TOKEN"
)

results = creator.create_all()
print(results)
EOF


#running metaobject definitions
python3 - << 'EOF'
from mvqueen_engine.brand_brain.metaobject_engine import MetaobjectDefinitionCreator

creator = MetaobjectDefinitionCreator("YOURSHOP.myshopify.com", "ACCESS_TOKEN")
print(creator.create_all())
EOF

#create a single definition
python3 - << 'EOF'
from mvqueen_engine.brand_brain.metaobject_engine import MetaobjectDefinitionCreator

creator = MetaobjectDefinitionCreator("YOURSHOP.myshopify.com", "ACCESS_TOKEN")
print(creator.create_definition("mvq_size_guide", []))
EOF

#creating metaobjects
python3 - << 'EOF'
from mvqueen_engine.brand_brain.metaobject_engine import MetaobjectCreator

creator = MetaobjectCreator("YOURSHOP.myshopify.com", "ACCESS_TOKEN")

fields = {
    "title": "Size Guide — Dresses",
    "body": "Measure bust, waist, hips.",
    "size_table": ["XS: 0–2", "S: 4–6", "M: 8–10"]
}

print(creator.create("mvq_size_guide", fields))
EOF


#running the product engine
python3 - << 'EOF'
from mvqueen_engine.brand_brain.product_engine import process_product

result = process_product(
    title="Luna Satin Mini Dress",
    description="A romantic satin mini dress with lace trim.",
    persona="The Dreamer",
    base_price=89.00,
    compare_at=129.00,
    size_guide_id="gid://shopify/Metaobject/123",
    ingredients_id=None,
    how_to_use_id=None,
    editorial_block_ids=[]
)

print(result["product_json"])
EOF

#syncing a product to shopify
python3 - << 'EOF'
from mvqueen_engine.brand_brain.product_engine import process_product
from mvqueen_engine.brand_brain.sync.product_sync import ProductSync

sync = ProductSync("YOURSHOP.myshopify.com", "ACCESS_TOKEN")

processed = process_product(
    title="Luna Satin Mini Dress",
    description="A romantic satin mini dress with lace trim.",
    persona="The Dreamer",
    base_price=89.00,
    compare_at=129.00,
)

created = sync.create_product(processed["product_json"])
product_id = created["product"]["id"]

sync.update_metafields(product_id, processed["metafields"])
EOF

#running a collection engine
python3 - << 'EOF'
from mvqueen_engine.brand_brain.collection_engine import process_collection

result = process_collection(
    title="Spring Romance Edit",
    theme="Soft Textures",
    persona="The Dreamer",
    season="Spring",
    vibe="Romantic"
)

print(result)
EOF


#syncing a collection
python3 - << 'EOF'
from mvqueen_engine.brand_brain.collection_engine import process_collection
from mvqueen_engine.brand_brain.sync.collection_sync import CollectionSync

sync = CollectionSync("YOURSHOP.myshopify.com", "ACCESS_TOKEN")

processed = process_collection(
    title="Spring Romance Edit",
    theme="Soft Textures",
    persona="The Dreamer",
    season="Spring",
    vibe="Romantic"
)

created = sync.create_collection(
    title="Spring Romance Edit",
    body_html=processed["editorial"]["long"]
)

collection_id = created["custom_collection"]["id"]

sync.update_metafields(collection_id, processed["metafields"])
EOF


#running the blog engine
python3 - << 'EOF'
from mvqueen_engine.brand_brain.blog_engine import process_blog

result = process_blog(
    title="How to Style Satin in Spring",
    topic="Satin Layering",
    persona="The Dreamer",
    season="Spring",
    vibe="Romantic",
    key_points=["Layering", "Textures", "Color Harmony"]
)

print(result)
EOF

#syncing a blog article
python3 - << 'EOF'
from mvqueen_engine.brand_brain.blog_engine import process_blog
from mvqueen_engine.brand_brain.sync.blog_sync import BlogSync

sync = BlogSync("YOURSHOP.myshopify.com", "ACCESS_TOKEN")

processed = process_blog(
    title="How to Style Satin in Spring",
    topic="Satin Layering",
    persona="The Dreamer",
    season="Spring",
    vibe="Romantic",
    key_points=["Layering", "Textures", "Color Harmony"]
)

created = sync.create_article(
    blog_id="123456789",
    title="How to Style Satin in Spring",
    body_html=processed["editorial"]["long"]
)

article_id = created["article"]["id"]

sync.update_metafields(article_id, processed["metafields"])
EOF


#running the page engine
python3 - << 'EOF'
from mvqueen_engine.brand_brain.page_engine import process_page

result = process_page(
    title="About MVQueen",
    page_type="About",
    brand_voice="Cinematic Luxury",
    core_message="Designed for women who lead with confidence."
)

print(result)
EOF



#syncing a page
python3 - << 'EOF'
from mvqueen_engine.brand_brain.page_engine import process_page
from mvqueen_engine.brand_brain.sync.page_sync import PageSync

sync = PageSync("YOURSHOP.myshopify.com", "ACCESS_TOKEN")

processed = process_page(
    title="About MVQueen",
    page_type="About",
    brand_voice="Cinematic Luxury",
    core_message="Designed for women who lead with confidence."
)

created = sync.create_page(
    title="About MVQueen",
    body_html=processed["editorial"]["long"]
)

page_id = created["page"]["id"]

sync.update_metafields(page_id, processed["metafields"])
EOF


#running the faq engine
python3 - << 'EOF'
from mvqueen_engine.brand_brain.faq_engine import process_faq_item

result = process_faq_item(
    question="How long is shipping?",
    answer="Shipping takes 3–5 business days.",
    category="Shipping"
)

print(result)
EOF


#syncing an faq as a metaobject
python3 - << 'EOF'
from mvqueen_engine.brand_brain.faq_engine import process_faq_item
from mvqueen_engine.brand_brain.sync.faq_sync import FAQSync

sync = FAQSync("YOURSHOP.myshopify.com", "ACCESS_TOKEN")

processed = process_faq_item(
    question="How long is shipping?",
    answer="Shipping takes 3–5 business days.",
    category="Shipping"
)

print(sync.create_faq(processed["editorial"]))
EOF


#running the navigation engine
python3 - << 'EOF'
from mvqueen_engine.brand_brain.navigation_engine import process_navigation
from mvqueen_engine.brand_brain.navigation_engine.menu_builder import build_menu_item

items = [
    build_menu_item("Shop All", "collection", "all"),
    build_menu_item("Dresses", "collection", "dresses"),
]

result = process_navigation(
    menu_title="Main Menu",
    persona="The Dreamer",
    season="Spring",
    vibe="Romantic",
    items=items
)

print(result)
EOF


#syncing navigation
python3 - << 'EOF'
from mvqueen_engine.brand_brain.navigation_engine import process_navigation
from mvqueen_engine.brand_brain.navigation_engine.menu_builder import build_menu_item
from mvqueen_engine.brand_brain.sync.navigation_sync import NavigationSync

sync = NavigationSync("YOURSHOP.myshopify.com", "ACCESS_TOKEN")

items = [
    build_menu_item("Shop All", "collection", "all"),
    build_menu_item("Dresses", "collection", "dresses"),
]

processed = process_navigation(
    menu_title="Main Menu",
    persona="The Dreamer",
    season="Spring",
    vibe="Romantic",
    items=items
)

sync.create_menu(processed["menu"])
EOF