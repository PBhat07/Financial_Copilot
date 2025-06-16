# financial_downloader.py
# This script downloads the latest 10-K filings for a list of companies
# from the SEC EDGAR database, converts them to PDF, and saves them
# to a specified Google Drive directory.

import requests
import json
import os
import time
import subprocess
from urllib.parse import urljoin

# --- Configuration ---
gdrive_base_path = '/content/drive/MyDrive/Financial_Copilot/data/financial_docs'

HEADERS = {
    'User-Agent': 'Financial_Copilot pbhat7799@gmail.com',  # Your specified User-Agent
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'data.sec.gov'
}

TARGET_TICKERS = [
    'AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'NVDA', 'META', 'JPM', 'V', 'UNH'
]

# --- Helper Functions ---
def get_cik_from_ticker(ticker_symbol):
    """Fetches the CIK (Central Index Key) for a given ticker symbol."""
    print(f"Looking up CIK for ticker: {ticker_symbol}")
    
    # Hardcoded CIK mapping for the target companies (as fallback)
    ticker_to_cik = {
        'AAPL': '0000320193',
        'MSFT': '0000789019', 
        'GOOG': '0001652044',
        'GOOGL': '0001652044',
        'AMZN': '0001018724',
        'TSLA': '0001318605',
        'NVDA': '0001045810',
        'META': '0001326801',
        'JPM': '0000019617',
        'V': '0001403161',
        'UNH': '0000731766'
    }
    
    # First try hardcoded mapping
    if ticker_symbol.upper() in ticker_to_cik:
        cik = ticker_to_cik[ticker_symbol.upper()]
        print(f"Found CIK from hardcoded mapping: {cik} for {ticker_symbol}")
        return cik
    
    # Try alternative URLs for company tickers
    urls_to_try = [
        "https://www.sec.gov/files/company_tickers.json",
        "https://data.sec.gov/files/company_tickers.json"
    ]
    
    for url in urls_to_try:
        try:
            print(f"Trying URL: {url}")
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            tickers_data = response.json()

            for company_info in tickers_data.values():
                if company_info['ticker'].upper() == ticker_symbol.upper():
                    cik = str(company_info['cik_str']).zfill(10)
                    print(f"Found CIK: {cik} for {ticker_symbol}")
                    return cik
            break  # If we get here, the URL worked but ticker wasn't found
            
        except requests.exceptions.RequestException as e:
            print(f"Error with URL {url}: {e}")
            continue
    
    print(f"CIK not found for ticker: {ticker_symbol}")
    return None

def get_latest_10k_url(cik):
    """
    Fetches the URL of the latest 10-K filing for a given CIK.
    Uses the data.sec.gov API to get filing information.
    """
    print(f"Fetching filings for CIK: {cik}")
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        company_filings = response.json()

        # Look through recent filings
        recent_filings = company_filings['filings']['recent']
        
        for i, form in enumerate(recent_filings['form']):
            if form == '10-K':
                accession_number = recent_filings['accessionNumber'][i]
                report_date = recent_filings['reportDate'][i]
                primary_document = recent_filings['primaryDocument'][i]
                
                # Remove hyphens from accession number for URL
                accession_no_hyphens = accession_number.replace('-', '')
                
                # Construct the document URL using the modern EDGAR structure
                doc_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_no_hyphens}/{primary_document}"
                
                # Verify the document exists
                try:
                    head_response = requests.head(doc_url, headers={
                        'User-Agent': 'Financial_Copilot pbhat7799@gmail.com',
                        'Accept-Encoding': 'gzip, deflate'
                    })
                    if head_response.status_code == 200:
                        print(f"Found 10-K at: {doc_url} (Date: {report_date})")
                        return doc_url, report_date, accession_number
                except requests.exceptions.RequestException:
                    print(f"Document not accessible: {doc_url}")
                    continue

        print(f"No accessible 10-K found for CIK: {cik}")
        return None, None, None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching filings for CIK {cik}: {e}")
        return None, None, None

def download_and_convert_to_pdf(ticker, output_dir):
    """
    Downloads the latest 10-K HTML, converts it to PDF, and saves it
    to the specified output directory.
    """
    cik = get_cik_from_ticker(ticker)
    if not cik:
        print(f"Skipping {ticker}: CIK not found.")
        return

    html_url, report_date, accession_number = get_latest_10k_url(cik)
    if not html_url:
        print(f"Skipping {ticker}: Could not find a suitable 10-K URL.")
        return

    # Create file paths
    temp_html_file_path = os.path.join("/tmp", f"{ticker}_10K_{accession_number.replace('-', '_')}.html")
    pdf_file_name = f"{ticker}_10K_{report_date}_{accession_number.replace('-', '_')}.pdf"
    pdf_file_path = os.path.join(output_dir, pdf_file_name)

    # Skip if PDF already exists
    if os.path.exists(pdf_file_path):
        print(f"PDF already exists for {ticker}: {pdf_file_path}. Skipping download and conversion.")
        return

    print(f"Downloading 10-K from: {html_url}")
    try:
        # Download the HTML file
        response = requests.get(html_url, headers={
            'User-Agent': 'Financial_Copilot pbhat7799@gmail.com',
            'Accept-Encoding': 'gzip, deflate'
        }, stream=True)
        response.raise_for_status()

        # Save temporary HTML file
        with open(temp_html_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"HTML downloaded to temporary path: {temp_html_file_path}")

        # First, save a permanent HTML copy as backup
        html_file_name = f"{ticker}_10K_{report_date}_{accession_number.replace('-', '_')}.html"
        html_file_path = os.path.join(output_dir, html_file_name)
        
        # Copy the temp HTML to permanent location
        import shutil
        shutil.copy2(temp_html_file_path, html_file_path)
        print(f"HTML file saved: {html_file_path}")
        
        # Try to convert HTML to PDF
        print(f"Converting to PDF: {pdf_file_path}")
        pdf_created = False
        
        # Method 1: Try wkhtmltopdf with local file
        try:
            subprocess.run([
                "wkhtmltopdf",
                "--disable-external-links",
                "--disable-forms",
                "--disable-plugins", 
                "--quiet",
                temp_html_file_path,
                pdf_file_path
            ], check=True, capture_output=True, text=True)
            print(f"Successfully converted and saved PDF: {pdf_file_path}")
            pdf_created = True
            
        except subprocess.CalledProcessError as e:
            print(f"wkhtmltopdf failed: {e.stderr}")
            
            # Method 2: Try with Python libraries (weasyprint or pdfkit alternative)
            try:
                print("Trying alternative PDF conversion method...")
                # Install weasyprint if available
                subprocess.run(["pip", "install", "weasyprint"], check=True, capture_output=True)
                import weasyprint
                
                # Read HTML content and convert
                with open(temp_html_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    html_content = f.read()
                
                # Create PDF with weasyprint
                html_doc = weasyprint.HTML(string=html_content, base_url='')
                html_doc.write_pdf(pdf_file_path)
                print(f"Successfully converted with weasyprint: {pdf_file_path}")
                pdf_created = True
                
            except Exception as e2:
                print(f"Alternative PDF conversion also failed: {e2}")
                print(f"HTML file is available at: {html_file_path}")
                print("You can manually convert HTML to PDF later if needed.")
        
        if not pdf_created:
            print(f"⚠️  PDF conversion failed for {ticker}, but HTML file is saved: {html_file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading 10-K for {ticker}: {e}")
    except Exception as e:
        print(f"Unexpected error processing {ticker}: {e}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_html_file_path):
            try:
                os.remove(temp_html_file_path)
                print(f"Cleaned up temporary file: {temp_html_file_path}")
            except OSError as e:
                print(f"Warning: Could not remove temporary file {temp_html_file_path}: {e}")

def install_wkhtmltopdf():
    """
    Install wkhtmltopdf if not available (for Google Colab environment)
    """
    try:
        subprocess.run(["wkhtmltopdf", "--version"], check=True, capture_output=True)
        print("wkhtmltopdf is already installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing wkhtmltopdf...")
        try:
            subprocess.run(["apt-get", "update"], check=True, capture_output=True)
            subprocess.run(["apt-get", "install", "-y", "wkhtmltopdf"], check=True, capture_output=True)
            print("wkhtmltopdf installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install wkhtmltopdf: {e}")
            print("Please install wkhtmltopdf manually or run in an environment where it's available")
            return False
    return True

# --- Main Execution Block ---
if __name__ == "__main__":
    print("\n--- Starting Document Download and Conversion for Target Companies ---")
    
    # Install wkhtmltopdf if needed
    if not install_wkhtmltopdf():
        print("Cannot proceed without wkhtmltopdf. Exiting.")
        exit(1)
    
    # Create output directory
    os.makedirs(gdrive_base_path, exist_ok=True)
    print(f"Saving documents to: {gdrive_base_path}")

    successful_downloads = 0
    for i, ticker in enumerate(TARGET_TICKERS, 1):
        print(f"\n--- Processing {ticker} ({i}/{len(TARGET_TICKERS)}) ---")
        try:
            download_and_convert_to_pdf(ticker, gdrive_base_path)
            successful_downloads += 1
        except Exception as e:
            print(f"Failed to process {ticker}: {e}")
        
        # Rate limiting: wait between requests
        if i < len(TARGET_TICKERS):
            print("Waiting 3 seconds before next request...")
            time.sleep(3)

    print(f"\n--- Process Complete ---")
    print(f"Successfully processed: {successful_downloads}/{len(TARGET_TICKERS)} companies")
    print(f"Check your directory at: {gdrive_base_path}")
    
    # List generated files
    if os.path.exists(gdrive_base_path):
        pdf_files = [f for f in os.listdir(gdrive_base_path) if f.endswith('.pdf')]
        html_files = [f for f in os.listdir(gdrive_base_path) if f.endswith('.html')]
        
        if pdf_files:
            print(f"\nGenerated PDF files ({len(pdf_files)}):")
            for pdf_file in sorted(pdf_files):
                file_path = os.path.join(gdrive_base_path, pdf_file)
                file_size = os.path.getsize(file_path)
                print(f"  - {pdf_file} ({file_size:,} bytes)")
        
        if html_files:
            print(f"\nGenerated HTML files ({len(html_files)}):")
            for html_file in sorted(html_files):
                file_path = os.path.join(gdrive_base_path, html_file)
                file_size = os.path.getsize(file_path)
                print(f"  - {html_file} ({file_size:,} bytes)")
        
        if not pdf_files and not html_files:
            print("\nNo files were generated. Check the error messages above.")
        
        print(f"\nNote: HTML files can be used directly in your RAG pipeline or converted to PDF later.")
        print(f"For RAG purposes, HTML files often work better as they preserve structure and formatting.")