import sys
import bs4
import requests
import os
import shutil
from pdfrw import PdfFileReader, PdfFileWriter


def download_files(links, directory):
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
    filtered_tags= []

    found_start = False
    found_end = False
    for item in tags:
        if str(item).find(start_date) >= 0:
            found_start = True
        if str(item).find(end_date) >= 0:
            found_end = True
        if found_start:
            filtered_tags.append(item)
            if found_end:
                break

    for item in filtered_tags:
        sublist = item.findAll("li", {"class": "ipf-nestedlist-file"})
        for subitem in sublist:
            links.append(base_url + subitem.a["href"])
    return links


def merge_pdfs(paths):
    writer = PdfFileWriter()
    for path in paths:
        reader = PdfFileReader(path)
        for i in range(len(reader.pages)):
            writer.addpage(reader.pages[i])
    writer.write("output.pdf")


if __name__ == "__main__":
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    links_ = get_pdf_links(start_date, end_date)
    paths = download_files(links_, "files/")
    merge_pdfs(paths)
    shutil.rmtree("files/")
