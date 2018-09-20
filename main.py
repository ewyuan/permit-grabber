import sys
import bs4
import requests
import os
import shutil
from pdfrw import PdfFileReader, PdfFileWriter


def download_files(links, directory):
    """
    Returns a list of strings that are the file paths to the downloaded PDFs from links.

    :param links: list[str]
    :param directory: str
    :return: list[str]
    """
    paths = []
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(len(links)):
        path = directory + str(i) + ".pdf"
        paths.append(path)
        response = requests.get(links[i])
        with open(path, 'wb') as f:
            f.write(response.content)
    return paths


def get_pdf_links(start_date, end_date):
    """
    Returns the direct link to download PDFs from "https://www.burnaby.ca/".
    This function parses the building permit web page and restricts the direct
    links outputted to be within the start_date and end_date.

    :param start_date: str
    :param end_date: str
    :return: list[str]
    """
    base_url = "https://www.burnaby.ca/"
    target_url = "https://www.burnaby.ca/City-Services/Building/Permits-Issued.html"
    links = []
    header = {'User-Agent': 'Mozilla/5.0 '
                            '(Windows NT 6.1; WOW64) '
                            'AppleWebKit/537.36 '
                            '(KHTML, like Gecko) '
                            'Chrome/56.0.2924.76 '
                            'Safari/537.36'}
    session = requests.get(url=target_url, headers=header)
    soup = bs4.BeautifulSoup(session.text, "html.parser")
    tags = soup.findAll("li", {"class": "ipf-nestedlist-folder"})
    found_start = False
    found_end = False
    for item in tags:
        sublist = item.findAll("li", {"class": "ipf-nestedlist-file"})
        for subitem in sublist:
            if str(subitem.text) == start_date:
                found_start = True
            if str(subitem.text) == end_date:
                found_end = True
            if found_start:
                links.append(base_url + subitem.a["href"])
                if found_end:
                    break

    return links


def merge_pdfs(paths):
    """
    Merges all the PDFs from the file paths from paths.

    :param paths: list[str]
    :return: None
    """
    writer = PdfFileWriter()
    for path in paths:
        reader = PdfFileReader(path)
        for i in range(len(reader.pages)):
            writer.addpage(reader.pages[i])
    writer.write("output.pdf")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 start_date end_date")
    else:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
        links_ = get_pdf_links(start_date, end_date)
        paths = download_files(links_, "files/")
        merge_pdfs(paths)
        shutil.rmtree("files/")
