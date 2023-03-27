# Bot analyze 1 on 2.

# Task 1.1: Overview of Bot Functionality and Goals
The goal of the Footlocker bot is to streamline the automated process of purchasing products from the online store. To check product availability, add items to the shopping cart and complete the transaction, it combines web scraping and API calls. The bot aims to speed up the purchase process and increase the likelihood of customers acquiring limited edition products.

To obtain a CSRF token, which is needed for subsequent requests, the bot sends an initial request to the Footlocker website. It then makes a series of requests to the website's APIs to search for products already in stock and obtain details about those products, including their ID, price and available sizes. The robot adds a product when it finds one that meets the requirements.

## Task 1.2: Technologies used by the robot
The bot was developed in JavaScript and uses a number of third-party libraries, including Got.js to send HTTP requests, xml2js to parse XML responses, and adyen-encryption-js to encrypt credit card data. Without a graphical user interface, the bot can communicate with the Footlocker website because it runs in a headless Node.js environment.

## Task 1.3: Techniques used to avoid detection
The bot uses several techniques to avoid detection by Footlocker's anti-bot measures. These techniques are as follows

Use of a proxy server: The bot is designed to route all requests through a proxy server, allowing it to hide its IP address and avoid being blocked by Footlocker's network security.

Setting custom headers: The bot places custom headers in its requests to mimic those of a legitimate web browser, including the user agent, acceptance headers and referrer.

Random Delays: The bot uses random delays between requests to avoid detection by Footlocker's anti-bot measures, which can be triggered by frequent or repetitive requests.

Encryption of sensitive data: The bot encrypts credit card information using the Adyen encryption library, which helps protect it from interception or detection by Footlocker security measures.

## Task 1.4: Potential Detection Methods


Monitoring for Unusual Traffic Patterns: Footlocker could monitor its website traffic for unusual patterns that indicate the presence of a bot, such as a high volume of requests from a single IP address or a large number of requests for a particular product.

Identify non-human browsing behaviors: Footlocker can use tools to identify browsing behaviors that are characteristic of bots, such as rapid clicking or scrolling, automatic form submissions, or use of keyboard shortcuts.

Identification of known bot IP addresses: Footlocker could maintain a list of known bot IP addresses and block traffic from those addresses.

Analysis of request headers: Footlocker could analyze the headers of requests sent by the bot to identify any inconsistencies or irregularities suggesting non-human traffic.

Overall, detecting and blocking bots is an ongoing challenge for online retailers, and requires a combination of technical measures and human monitoring to be effective.

## Areas for Improvement

- Use random delays between requests to mimic human behavior and avoid triggering throughput limits.

- Randomize the order of actions performed on the website, as this can make it harder for anti-bot measures to detect patterns.

- Use a variety of user agents, IP addresses and other identifying information to make it harder to trace requests back to the bot.

- Use a webscraper.py-based bot with these multiple user_agents or browsing automation tools that more closely resemble human browsing behavior, rather than relying solely on HTTP requests.

- Avoid pulling large amounts of data from the website in a short period of time, as this can easily trigger rate limits or other anti-bot measures.
