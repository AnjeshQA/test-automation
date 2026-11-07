# Adnabu Store - Web Automation Assessment (BDD)

This repository contains a professional automated testing suite for the Adnabu Shopify store recruitment assessment. The framework is built using **Python**, **Selenium WebDriver**, and **Pytest-BDD**, following the **Page Object Model (POM)** design pattern.

## 🏗️ Framework Architecture
- **Design Pattern:** Page Object Model (POM) for enhanced maintainability.
- **Methodology:** Behavior Driven Development (BDD) using Gherkin syntax.
- **Data-Driven:** All locators and test data (URLs, Passwords, Product Names) are managed externally in `Utilities/config.ini`.
- **Dynamic Logic:** Implemented dynamic XPATH formatting to interact with products based on configuration data.

## 🧩 Feature Coverage
The test suite automates the following end-to-end user journey:
1. **Security Bypass:** Automatically enters the Shopify store password to gain access.
2. **Product Search:** Opens the search modal and queries the product name defined in the config file.
3. **Cart Management:** Identifies the correct product from search results and adds it to the cart.
4. **Checkout Verification:** Validates the transition to the checkout summary and ensures the "Pay Now" button is present.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/AnjeshQA/test-automation.git
cd adnabu-store-assignment



### 2. Create a Virtual Environment
```bash
# Create the virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
# venv\Scripts\activate

### 3. Install Dependencies
```bash
pip install -r requirements.txt

### 4. Standard Execution (with Allure Results)
pytest AddToCartAssessment/TestCases/test_shopProductCheckout_bdd.py --alluredir=allure-results


### 5. Generate Allure Report
```bash
allure serve allure-results



Project Structure:
AddToCartAssessment/Features/: Gherkin feature files defining test scenarios.

AddToCartAssessment/TestCases/: Pytest-BDD step definitions (Python glue code).

Pages/: Page Object classes containing Selenium element interactions.

Utilities/: Configuration readers and the config.ini file.

requirements.txt: List of all necessary Python libraries.