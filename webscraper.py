try:
    import sys
    import os
    import random
    import asyncio
    import datetime
    from urllib.parse import urlparse, urljoin

    import aiofiles
    import aiohttp
    from bs4 import BeautifulSoup
    from weasyprint import HTML
    import argparse

except ImportError as e:
    print(f"ImportError: {e}")
    print("Trying to install missing packages...")

    try:
        import pip
    except ImportError:
        print("pip is not installed. Please install pip.")
        sys.exit(1)

    packages = ["aiofiles", "aiohttp", "beautifulsoup4", "weasyprint"]

    for package in packages:
        try:
            __import__(package)
        except ImportError:
            pip.main(["install", package])

    print("All missing packages installed. Please run the script again.")


class WebScraper:
    def __init__(self, headers_file, concurrent_requests, output_dir):
        self.headers_list = self.load_headers(headers_file)
        self.concurrent_requests = concurrent_requests
        self.output_dir = output_dir

    def load_headers(self, headers_file: object) -> object:
        """
             A method that loads user agent headers from a file and returns them as a list.
        :param headers_file:
        """
        headers_list = []
        with open(headers_file, "r") as file:
            for line in file:
                headers_list.append(eval(line.strip()))
        return headers_list

    def get_random_headers(self) -> object:
        """
        A method that selects a random user agent header from the list of headers loaded from the file
        """
        return random.choice(self.headers_list)

    async def save_page(self, url: object, content: object) -> object:
        """
        An asynchronous method that saves the HTML content of a scraped webpage to a file, using the URL of the webpage to generate a unique filename.
        :param url:
        :param content:
        """
        filename = os.path.join(self.output_dir, f"{url.replace('/', '_')}.html")
        async with aiofiles.open(filename, "w") as file:
            await file.write(content)

    async def save_report(self, url: object, report: object, format: object) -> object:
        """
        An asynchronous method that saves a report generated for a scraped webpage to a file, using the URL of the webpage to generate a unique filename, and the specified report format.
        :param url:
        :param report:
        :param format:
        """
        filename = os.path.join(
            self.output_dir, f"{url.replace('/', '_')}_report.{format}"
        )
        if format.lower() == "pdf":
            async with aiofiles.open(filename, "wb") as file:
                await file.write(report)
        else:
            async with aiofiles.open(filename, "w") as file:
                await file.write(report)

    async def scrape_and_generate_report(self, url: object, session: object) -> object:
        """
        An asynchronous method that scrapes a webpage, generates a report for the webpage, and saves the report to a file. It uses a specified user agent header for the request, and a specified report format for the report.
        :param url:
        :param session:
        """
        headers = self.get_random_headers()
        try:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    content = await response.text()
                    await self.save_page(url, content)
                    print(f"Scraped {url}")

                    soup = BeautifulSoup(content, "html.parser")
                    report_generator = ReportGenerator(soup, url)

                    # Generate report in the specified format
                    if report_format.lower() == "html":
                        report = report_generator.generate_html_report()
                        await self.save_report(url, report, "html")
                    elif report_format.lower() == "pdf":
                        report = report_generator.generate_pdf_report()
                        await self.save_report(url, report, "pdf")
                    elif report_format.lower() == "csv":
                        report = report_generator.generate_csv_report()
                        await self.save_report(url, report, "csv")
                    else:
                        print(f"Invalid report format: {report_format}")
                else:
                    print(f"Failed to scrape {url} - Status code: {response.status}")
        except aiohttp.ClientError as e:
            print(f"Failed to scrape {url} - Error: {str(e)}")

    async def scrape_urls(self, urls: object, report_format: object) -> object:
        """
            An asynchronous method that scrapes a list of webpages, generates reports for the webpages, and saves the reports to files. It uses a specified user agent header for the requests, and a specified report format for the reports.
        :param urls:
        :param report_format:
        """
        headers = self.get_random_headers()
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = [self.scrape_and_generate_report(url, session) for url in urls]
            await asyncio.gather(*tasks)


class ReportGenerator:
    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self.timestamp = datetime.datetime.now()

    def generate_html_report(self) -> object:
        """
        A method that generates an HTML report for a scraped webpage, containing information about the webpage's internal and external links, images, and HTML tag count.
        :return:
        """
        internal_links, external_links = self._get_links()
        images = self._get_images
        tags = ["a", "div", "p", "h1", "h2", "h3", "h4", "h5", "h6"]

        report_sections = [
            self._generate_header_section(),
            self._generate_links_section(internal_links, external_links),
            self._generate_images_section(images),
            self._generate_tag_count_section(tags),
        ]

        return "\n".join(report_sections)

    def _generate_header_section(self) -> str:
        """A method that generates an HTML header section for the HTML report, containing the URL of the webpage being reported on, and a timestamp."""
        return f"<h1>Report for {self.url}</h1>\n<p>Timestamp: {self.timestamp}</p>"

    def _generate_links_section(
        self, internal_links: object, external_links: object
    ) -> object:
        """A method that generates an HTML section for the HTML report, containing information about the internal and external links found on the scraped webpage."""
        links_section = ["<h2>Links</h2>", "<ul>"]

        for link_type, links in [
            ("Internal", internal_links),
            ("External", external_links),
        ]:
            for link in links:
                links_section.append(
                    f'<li>{link_type}: <a href="{link}">{link}</a></li>'
                )

        links_section.append("</ul>")
        return "\n".join(links_section)

    def _generate_images_section(self, images: object) -> str:
        """
        A method that generates an HTML section for the HTML report, containing information about the images found on the scraped webpage.
        :param images:
        :return:
        """
        images_section = ["<h2>Images</h2>", "<ul>"]

        for image in images:
            images_section.append(f'<li><img src="{image}" alt="Image" /></li>')

        images_section.append("</ul>")
        return "\n".join(images_section)

    def _generate_tag_count_section(self, tags: object) -> object:
        """
         A method that generates an HTML section for the HTML report, containing information about the HTML tag count for the scraped webpage.
        :rtype: object
        """
        tag_count_section = [
            "<h2>HTML Tag Count</h2>",
            "<table>",
            "<thead><tr><th>Tag</th><th>Count</th></tr></thead>",
            "<tbody>",
        ]

        for tag in tags:
            count = len(self.soup.find_all(tag))
            tag_count_section.append(f"<tr><td>{tag}</td><td>{count}</td></tr>")

        tag_count_section.extend(["</tbody>", "</table>"])
        return "\n".join(tag_count_section)

    def generate_pdf_report(self) -> object:
        """
        A method that generates a PDF report for a scraped webpage, using the HTML report generated by the
        :return:
        """
        html_report = self.generate_html_report()
        pdf_report = HTML(string=html_report).write_pdf()
        return pdf_report

    def generate_csv_report(self) -> object:
        """
        A method that generates a CSV report for a scraped webpage, containing information about the webpage's internal and external links, images, and HTML tag count.
                :return:
        """
        internal_links, external_links = self._get_links()
        images = self._get_images

        report = [
            f"URL,{self.url}",
            f"Timestamp,{self.timestamp}",
            "Type,Link",
        ]

        for link in internal_links:
            report.append(f"Internal,{link}")
        for link in external_links:
            report.append(f"External,{link}")

        report.append("Images")
        for image in images:
            report.append(f"Image,{image}")

        report.append("HTML Tag Count")
        tags = ["a", "div", "p", "h1", "h2", "h3", "h4", "h5", "h6"]
        for tag in tags:
            count = len(self.soup.find_all(tag))
            report.append(f"{tag},{count}")

        return "\n".join(report)

    def _get_links(self) -> object:
        """
        A method that returns a tuple of sets, containing the internal and external links found on a scraped webpage.
        :return:
        """
        internal_links = set()
        external_links = set()

        for a_tag in self.soup.find_all("a", href=True):
            link = a_tag["href"]
            if self._is_external_link(link):
                external_links.add(link)
            else:
                internal_links.add(urljoin(self.url, link))

        return internal_links, external_links

    @property
    def _get_images(self) -> object:
        """
        A method that returns a set of image URLs found on a scraped webpage.
        :return:
        """
        images = set()

        for img_tag in self.soup.find_all("img", src=True):
            src = img_tag["src"]
            images.add(urljoin(self.url, src))

        return images

    def _is_external_link(self, link: object) -> bool:
        """
        A method that returns a boolean value indicating whether a given link is external to the domain of the scraped webpage.
        :param link:
        :return:
        """
        netloc = urlparse(link).netloc
        return bool(netloc) and netloc != urlparse(self.url).netloc


def parse_arguments() -> object:
    """
    A function that uses the argparse module to parse command-line arguments passed to the script, and returns them as an argparse.Namespace object.
    :return:
    """
    parser = argparse.ArgumentParser(description="Web scraper with report generation.")
    parser.add_argument(
        "-u", "--urls", nargs="+", required=True, help="List of URLs to scrape."
    )
    parser.add_argument(
        "-hf",
        "--headers_file",
        default="user_agents.txt",
        help="File containing user agent headers.",
    )
    parser.add_argument(
        "-c",
        "--concurrent_requests",
        type=int,
        default=10,
        help="Number of concurrent requests.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        default="scraped_pages",
        help="Directory to save scraped pages and reports.",
    )
    parser.add_argument(
        "-rf",
        "--report_format",
        default="csv",
        help="Format of the report (html, pdf, or csv).",
    )

    return parser.parse_args()


def print_banner():
    """
    A function that prints a banner containing the name of the program, and the version number and programming language used.
    :return:
    """
    banner = """
            __        _______ ____    ____   ____ ____      _    ____  _____ ____  _ 
        \ \      / / ____| __ )  / ___| / ___|  _ \    / \  |  _ \| ____|  _ \| |
         \ \ /\ / /|  _| |  _ \  \___ \| |   | |_) |  / _ \ | |_) |  _| | |_) | |
          \ V  V / | |___| |_) |  ___) | |___|  _ <  / ___ \|  __/| |___|  _ <|_|
           \_/\_/  |_____|____/  |____/ \____|_| \_\/_/   \_\_|   |_____|_| \_(_)
   """
    print(banner)
    print("            Scrappy Test 1.0 beta - Powered by Python 3")


if __name__ == "__main__":
    print_banner()
    try:
        args = parse_arguments()

        headers_file = args.headers_file
        concurrent_requests = args.concurrent_requests
        output_dir = args.output_dir
        report_format = args.report_format

        os.makedirs(output_dir, exist_ok=True)

        urls = args.urls

        scraper = WebScraper(headers_file, concurrent_requests, output_dir)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(scraper.scrape_urls(urls, report_format))

    except KeyboardInterrupt:
        print("User interrupted the program.")
        sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)
    finally:
        print("Did you just tried to launch me without arguments :'(  [?] ")
        loop.close()
