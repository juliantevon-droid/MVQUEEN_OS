# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — TEST HARNESS (BLOCK K)
# ---------------------------------------------------------

from mvqueen_engine.engine import run

SAMPLE_INPUTS = [
    "Black satin slip dress with lace trim",
    "Oversized wool coat with structured shoulders",
    "Soft glam hydrating serum for glowing skin",
    "High-waisted denim with raw hem and silver hardware",
]


def run_tests():
    """
    Runs the Omniluxe Engine against a set of sample inputs.
    Returns a list of full engine outputs:
        {
            "product": {...},
            "csv_row": {...}
        }
    """
    results = []
    for text in SAMPLE_INPUTS:
        results.append(run(text))
    return results


def print_test_results():
    """
    Pretty-print key fields from the test results.
    """
    for result in run_tests():
        product = result["product"]

        print("\n----------------------------------------")
        print("INPUT:", product["input_text"])
        print("TITLE:", product["title"])
        print("HANDLE:", product["handle"])
        print("CATEGORY:", product["category"])
        print("PRODUCT TYPE:", product["product_type"])
        print("PERSONA:", product["persona"])
        print("TREND:", product["trend"])
        print("SEASON:", product["season"])
        print("VIBE:", product["vibe"])
        print("MATERIAL:", product["material"])
        print("SILHOUETTE:", product["silhouette"])
        print("DETAIL:", product["detail"])
        print("EDITORIAL SHORT:", product["editorial_short"])
        print("ALT TEXT SHORT:", product["alt_text_short"])
        print("SEO PRIMARY:", product["seo_primary"])
        print("TAGS:", product["tags"])
        print("COLLECTIONS:", product["collections"])
        print("PRICE:", product["price"])
        print("----------------------------------------\n")