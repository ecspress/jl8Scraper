"""Scrapes the JL8 comic site and creates a cbr file"""

from html_tag_parser import HTMLTagParser
import urllib.parse
import urllib.error
import urllib.request
import zipfile

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3"

def fetch_url(url):
    """Fetches the URL using firefox 27 user-agent.

    Input:
        URL

    Output:
        URL content as bytes.

    Raises:
        None
    """
    headers = {"User-Agent":USER_AGENT}
    page_request = urllib.request.Request(url, headers=headers)
    try:
        page_response = urllib.request.urlopen(page_request)
        if page_response.geturl() != url:
            print("Page redirects to previous entry")
            return None
    except urllib.error.HTTPError as error:
        print("Unable to access %s: HTTP error code %d", url, error.code)
        return None
    except urllib.error.URLError as error:
        print("Unable to read %s: Reason %s", url, error.reason)
        return None
    else:
        return page_response.read()

def parse_page(url, image_file):
    """Parses page and looks for images and next page link"""
    print("Parsing page", url, sep=" -> ")
    page_content = fetch_url(url)
    if page_content:
        data = page_content.decode("utf-8")
        data = data.replace("&lt;", 'previous')
        data = data.replace("&gt;", 'next')
        #data = data.replace("\n", '')
        #data = data.replace("\t", '')
        #data = data.replace("&nbsp;", '')
        #data = data.replace("&middot;", '')
        #data = data.replace("&copy;", '')
        parser = HTMLTagParser()
        parser.parse(data)
        for image in parser.images:
            atrs = image.attributes
            if atrs and atrs.get("alt") and atrs["alt"] == "Comic":
                download_image(image.attributes["src"], image_file)
        for link in parser.links:
            if link.attributes and link.data and link.data == "next":
                parse_page(link.attributes["href"], image_file)

def download_image(url, image_file):
    """Downloads image"""
    image_name = url.split('/')[-1]

    page_content = fetch_url(url)
    with zipfile.ZipFile(image_file, "a") as comic:
        comic.writestr(image_name, data=page_content)
    print("Downloaded image", image_name, sep=" -> ")

def find_last_image(image_file):
    """Finds the last image in image folder"""
    with zipfile.ZipFile(image_file, 'a') as comic:
        files = comic.namelist()

        if len(files) == 0:
            return 0
        else:
            files = [int(x.split('.')[0].split('_')[0]) for x in files]
            files.sort()
            return files[-1]

def main():
    """Runs the current module"""
    try:
        image_file = "./jl8_comic.cbr"
        last_image = find_last_image(image_file)

        site = "http://limbero.org/jl8/"
        url = urllib.parse.urljoin(site, str(last_image + 1))
        parse_page(url, image_file)
    except KeyboardInterrupt:
        print("Exit keyboard combo detected: Exiting....")


if __name__ == "__main__":
    main()
