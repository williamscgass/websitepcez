import requests
from bs4 import BeautifulSoup
import json
from openai import OpenAI
from urllib.parse import urlparse, urlunparse
from backend.mongodb.write import track_price



def fetch_title_and_price_from_html(url):
    """
    Fetch the title and price from a webpage.

    :param url: str, the URL of the webpage
    :return: tuple, the title and price extracted from the HTML
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title_tag = soup.find("h1", class_="heading-4 leading-6 font-500")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"

        # Extract the price
        price_tag = soup.find("div", class_="priceView-hero-price priceView-customer-price")
        price_span = price_tag.find("span", {"aria-hidden": "true"}) if price_tag else None
        price = price_span.get_text(strip=True) if price_span else "Price not found"

        return title, price
    except Exception as e:
        print(f"Error fetching title and price: {e}")
        return None, None

def extract_model_with_bs4(url):
    """
    Extract the model from the product webpage.

    :param url: str, the URL of the product page
    :return: str, the extracted model or an error message
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the element with the class 'product-data-value'
        model_element = soup.find('span', {'class': 'product-data-value'})
        
        # Extract and return the text
        if model_element:
            return model_element.text.strip()
        else:
            return "Model information not found."

    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"

def extract_pc_parts_from_title_and_price(title, price):
    """
    Use GPT to extract PC parts and price from the title and price.

    :param title: str, the title of the product
    :param price: str, the price of the product
    :return: dict, extracted information in a structured JSON format
    """
    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": (
                        f"Extract the PC parts and price from the following information:\n\n"
                        f"Title: {title}\nPrice: {price}\n\n"
                        f"Return the output as a JSON object with keys: 'title', 'processor', 'memory', 'graphics_card', 'storage', 'color', and 'price'."
                    )
                }
            ]
        )

        # Handle response and parse JSON
        response_content = completion.choices[0].message.content.strip()

        # Strip Markdown code fences if present
        if response_content.startswith("```json") and response_content.endswith("```"):
            response_content = response_content[7:-3].strip()

        return json.loads(response_content)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return {"error": "Failed to parse JSON from OpenAI API response"}
    except Exception as e:
        print(f"Error extracting PC parts and price: {e}")
        return {"error": str(e)}

from urllib.parse import urlparse, urlunparse

def remove_url_fluff(url):
    """
    Removes search parameters and fragments from a given URL while retaining the main path and domain.

    :param url: str, the full URL to process
    :return: str, the cleaned URL without search parameters and fragments
    """
    try:
        # Parse the URL
        parsed_url = urlparse(url)

        # Remove query and fragment
        cleaned_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))

        return cleaned_url.rstrip('/')  # Remove trailing slashes for consistency
    except Exception as e:
        print(f"Error processing URL: {e}")
        return None



# Example usage


url = "https://www.bestbuy.com/site/cyberpowerpc-gamer-xtreme-gaming-desktop-intel-core-i7-14700f-16gb-memory-nvidia-geforce-rtx-4060-ti-8gb-2tb-ssd-black/6575073.p"
title, price = fetch_title_and_price_from_html(url)
print(title)
if title and price:
    pc_parts_and_price = extract_pc_parts_from_title_and_price(title, price)
    parts = {'processor': pc_parts_and_price['processor'], 'memory':pc_parts_and_price['memory'],'graphics_card':pc_parts_and_price['graphics_card'],
             'storage':pc_parts_and_price['storage']}
    del(pc_parts_and_price['color'])
    print(pc_parts_and_price)
    if isinstance(pc_parts_and_price, dict):  # Ensure it's a dictionary
        pc_parts_and_price['model'] = extract_model_with_bs4(url)
        pc_parts_and_price['url'] = remove_url_fluff(url)
        print("success")
        track_price("prebuilts","bestbuy",pc_parts_and_price["model"],pc_parts_and_price["title"],pc_parts_and_price['price'],
                    pc_parts_and_price['url'], parts)
    else:
        print("Error: Expected a dictionary but got:", type(pc_parts_and_price))
else:
    print("Failed to fetch title and/or price from the URL.")
