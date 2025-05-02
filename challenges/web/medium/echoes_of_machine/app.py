from flask import Flask, request, render_template
import random
import string

app = Flask(__name__)

reviews_db = {
    "Quantum Widget": []
}

FLAG = "FLAG{LLM_OUTPUT_G0NE_WILD}"

def llm_generate_response(product, include_reviews=False):
    base_response = f"The {product} is a cutting-edge device with quantum capabilities."
    if include_reviews and product in reviews_db:
        reviews = reviews_db[product]
        if reviews:
            review_text = "\n".join(reviews)
            if "fetch_internal_info()" in review_text or "/admin/flag" in review_text:
                return f"{base_response}\nReviews:\n{review_text}\nInternal Data: {FLAG}"
            return f"{base_response}\nReviews:\n{review_text}"
    return base_response

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        query = request.form.get("query", "")
        product = "Quantum Widget"
        include_reviews = "review" in query.lower()
        response = llm_generate_response(product, include_reviews)
    return render_template("index.html", response=response)

@app.route("/submit_review", methods=["POST"])
def submit_review():
    review = request.form.get("review", "")
    product = "Quantum Widget"
    if review and len(reviews_db[product]) < 10:  
        reviews_db[product].append(review)
        return "Review submitted successfully!"
    return "Review submission failed (limit reached or empty)."

@app.route("/admin/flag")
def admin_flag():
    if request.remote_addr == "127.0.0.1":
        return [FLAG,request.remote_addr]
    return "Access denied."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)